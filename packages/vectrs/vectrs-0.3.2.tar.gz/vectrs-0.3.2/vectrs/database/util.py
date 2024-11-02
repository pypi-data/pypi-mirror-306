import hashlib
import numpy as np
import logging
from typing import List, Dict, Any

def generate_hash_id(input_id: str) -> str:
    return hashlib.sha256(input_id.encode()).hexdigest()

def normalize_vector(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        logging.warning("Attempt to normalize a zero vector.")
        return vector
    return vector / norm

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

def validate_positive_integer(value: int, variable_name: str = "variable"):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{variable_name} must be a positive integer, got {value}.")

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return np.linalg.norm(a - b)

def inner_product(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b)

def validate_metadata(metadata: Dict[str, Any]):
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary")
    for key, value in metadata.items():
        if not isinstance(key, str):
            raise ValueError("Metadata keys must be strings")
        if not isinstance(value, (str, int, float, bool)):
            raise ValueError("Metadata values must be primitive types (str, int, float, bool)")

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]