import json
import gzip
import lz4.frame
import numpy as np
from multiprocessing import Pool, cpu_count
from datasets import load_dataset
from typing import List, Callable, Optional

class ZIPFIT:
    def __init__(
        self, 
        jsonl_file_path: str, 
        target_dataset_name: str, 
        target_load_fn: Callable[[str], List[str]], 
        target_parse_fn: Callable[[dict], str], 
        k: int,
        output_file: str = "top_k_sequences.jsonl",
        compression_algorithm: str = 'gzip'
    ):
        self.jsonl_file_path = jsonl_file_path
        self.target_dataset_name = target_dataset_name
        self.target_load_fn = target_load_fn
        self.target_parse_fn = target_parse_fn
        self.output_file = output_file
        self.compress_cache = {}
        self.k = k
        self.compression_algorithm = compression_algorithm
        
        """
        Initializes the ZIPFIT instance.

        Parameters:
        - jsonl_file_path (str): Path to the input JSONL file containing source sequences.
        - target_dataset_name (str): Name of the target dataset to load from Hugging Face.
        - target_load_fn (Callable): Function to load the target dataset.
        - target_parse_fn (Callable): Function to parse examples from the target dataset (optional).
        - k (int): Number of top sequences to output.
        - output_file (str): Name of the output file for the top K sequences (default: "top_k_sequences.jsonl").
        - compression_algorithm (str): Compression algorithm to use ('gzip' or 'lz4').
        """
    def load_jsonl(self) -> List[str]:
        """Loads and returns the text field from a JSONL file.

        Returns:
            List[str]: A list of text entries from the JSONL file.
        """
        data = []
        try:
            with open(self.jsonl_file_path, 'r') as f:
                for line in f:
                    item = json.loads(line)
                    data.append(item['text']) 
        except FileNotFoundError:
            print(f"Error: The file {self.jsonl_file_path} was not found.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")
        return data


    def load_and_process_datasets(self) -> list:
        """Loads a subset of a dataset from Hugging Face or JSONL.

        Returns:
            list: A list of processed sequences from the target dataset.
        """
        if self.target_load_fn:
            return self.target_load_fn(self.target_dataset_name)
        else:
            # If the target dataset is a JSONL file, load it directly
            return self.load_jsonl(self.target_dataset)

    def compress(self, data: str) -> int:
        """Compresses the input data using the specified algorithm and returns the size of the compressed data, using a cache.

        Parameters:
            data (str): The input data to compress.

        Returns:
            int: The size of the compressed data.
        """
        if data in self.compress_cache:
            return self.compress_cache[data]
        
        if self.compression_algorithm == 'gzip':
            compressed_size = len(gzip.compress(data.encode('utf-8'), compresslevel=1))
        elif self.compression_algorithm == 'lz4':
            compressed_size = len(lz4.frame.compress(data.encode('utf-8')))
        else:
            raise ValueError(f"Unsupported compression algorithm: {self.compression_algorithm}")

        self.compress_cache[data] = compressed_size  # Cache the result
        return compressed_size

    def normalized_compression_distance(self, c1: int, c2: int, c12: int) -> float:
        """Calculates the Normalized Compression Distance given precomputed compression sizes.

        Parameters:
            c1 (int): The compressed size of the first sequence.
            c2 (int): The compressed size of the second sequence.
            c12 (int): The compressed size of the concatenated sequences.

        Returns:
            float: The normalized compression distance.
        """
        return (c12 - min(c1, c2)) / max(c1, c2)

    def similarity(self, args) -> float:
        """Calculates similarity based on the normalized compression distance.

        Parameters:
            args (tuple): A tuple containing two sequences and their compressed sizes.

        Returns:
            float: The similarity score between the two sequences.
        """
        s1, s2, c1, c2 = args
        c12 = self.compress(s1 + s2)  # Use the cached compress function
        return 1 - self.normalized_compression_distance(c1, c2, c12)

    # Precompute GZIP sizes for each dataset
    def precompute_gzip_sizes(self, data):
        """Precompute the GZIP sizes for each sequence in the dataset.

        Parameters:
            data (list): A list of sequences to compress.

        Returns:
            list: A list of compressed sizes for the input sequences.
        """
        with Pool(cpu_count()) as pool:
            return pool.map(self.compress, data, chunksize = 2000)

    def rank_sequences_by_alignment(self, mixed_data: list, reference_data: list) -> list:
        """Ranks sequences by alignment with reference data using dynamic scheduling.

        Parameters:
            mixed_data (list): A list of mixed data sequences.
            reference_data (list): A list of reference data sequences.

        Returns:
            list: A list of top K sequences with their alignment scores.
        """
        mixed_compressed = self.precompute_gzip_sizes(mixed_data)
        ref_compressed = self.precompute_gzip_sizes(reference_data)
        scores = []
        with Pool(cpu_count()) as pool:
            args_list = [(seq, ref, mixed_compressed[i], ref_compressed[j]) 
                        for i, seq in enumerate(mixed_data) 
                        for j, ref in enumerate(reference_data)]
            
            # Dynamic scheduling of similarity computation
            results = pool.imap_unordered(self.similarity, args_list, chunksize=2000)
            
            for result in results:
                scores.append(result)

        data_with_scores = list(zip(mixed_data, scores))
        top_k = sorted(data_with_scores, key=lambda x: x[1], reverse=True)[:self.k]
        return top_k
        

    def run(self):
        """Main execution function to run the data processing and scoring."""
        mixed_data = self.load_jsonl()
        reference_data = self.load_and_process_datasets() 
        top_k = self.rank_sequences_by_alignment(mixed_data, reference_data)

        # Create a new JSONL file with the top K sequences
        with open(self.output_file, 'w') as f:
            for text, score in top_k:
                f.write(json.dumps({'text': text, 'alignment_score': score}) + '\n')

        print(f"Top {self.k} sequences saved to {self.output_file}")

