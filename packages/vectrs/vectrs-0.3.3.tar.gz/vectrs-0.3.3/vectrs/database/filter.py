import numpy as np
from typing import List, Tuple, Dict, Any, Callable

class Filter:
    # This class might include methods for complex querying
    pass

def apply_filters(vectors: List[Tuple[str, np.ndarray]], filters: Dict[str, Any]) -> List[Tuple[str, np.ndarray]]:
    filtered_vectors = []
    for vector_id, vector in vectors:
        if all(apply_filter(vector, filter_name, filter_value) for filter_name, filter_value in filters.items()):
            filtered_vectors.append((vector_id, vector))
    return filtered_vectors

def apply_filter(vector: np.ndarray, filter_name: str, filter_value: Any) -> bool:
    filter_functions = {
        'min_norm': lambda v, val: np.linalg.norm(v) >= val,
        'max_norm': lambda v, val: np.linalg.norm(v) <= val,
        'min_value': lambda v, val: np.min(v) >= val,
        'max_value': lambda v, val: np.max(v) <= val,
        'dimension': lambda v, val: len(v) == val,
    }
    return filter_functions.get(filter_name, lambda v, val: True)(vector, filter_value)

def filter_by_metadata(vectors: List[Tuple[str, np.ndarray, Dict[str, Any]]], metadata_filters: Dict[str, Any]) -> List[Tuple[str, np.ndarray, Dict[str, Any]]]:
    return [
        (vector_id, vector, metadata)
        for vector_id, vector, metadata in vectors
        if all(
            metadata.get(key) == value
            for key, value in metadata_filters.items()
        )
    ]

def range_filter(vectors: List[Tuple[str, np.ndarray, Dict[str, Any]]], field: str, min_value: float, max_value: float) -> List[Tuple[str, np.ndarray, Dict[str, Any]]]:
    return [
        (vector_id, vector, metadata)
        for vector_id, vector, metadata in vectors
        if min_value <= float(metadata.get(field, 0)) <= max_value
    ]

def text_search_filter(vectors: List[Tuple[str, np.ndarray, Dict[str, Any]]], field: str, query: str) -> List[Tuple[str, np.ndarray, Dict[str, Any]]]:
    return [
        (vector_id, vector, metadata)
        for vector_id, vector, metadata in vectors
        if query.lower() in str(metadata.get(field, '')).lower()
    ]

def composite_filter(vectors: List[Tuple[str, np.ndarray, Dict[str, Any]]], filters: List[Callable]) -> List[Tuple[str, np.ndarray, Dict[str, Any]]]:
    for filter_func in filters:
        vectors = filter_func(vectors)
    return vectors

def apply_filters_efficiently(vectors: List[Tuple[str, np.ndarray]], min_norm: float = None, max_norm: float = None) -> List[Tuple[str, np.ndarray]]:
    vector_ids, vector_array = zip(*vectors)
    vector_array = np.array(vector_array)
    norms = np.linalg.norm(vector_array, axis=1)
    condition = np.ones_like(norms, dtype=bool)
    if min_norm is not None:
        condition &= (norms >= min_norm)
    if max_norm is not None:
        condition &= (norms <= max_norm)
    filtered_vectors = [(vector_ids[i], vector_array[i]) for i in range(len(vector_ids)) if condition[i]]
    return filtered_vectors

def filter_by_id(vectors: List[Tuple[str, np.ndarray]], target_ids: set) -> List[Tuple[str, np.ndarray]]:
    return [vector for vector in vectors if vector[0] in target_ids]

def apply_complex_filters(vectors: List[Tuple[str, np.ndarray, Dict[str, Any]]], filters: Dict[str, Any]) -> List[Tuple[str, np.ndarray, Dict[str, Any]]]:
    filtered_vectors = []
    for vector_id, vector, metadata in vectors:
        if all(apply_complex_filter(vector, metadata, filter_name, filter_value) for filter_name, filter_value in filters.items()):
            filtered_vectors.append((vector_id, vector, metadata))
    return filtered_vectors

def apply_complex_filter(vector: np.ndarray, metadata: Dict[str, Any], filter_name: str, filter_value: Any) -> bool:
    filter_functions = {
        'min_norm': lambda v, m, val: np.linalg.norm(v) >= val,
        'max_norm': lambda v, m, val: np.linalg.norm(v) <= val,
        'min_value': lambda v, m, val: np.min(v) >= val,
        'max_value': lambda v, m, val: np.max(v) <= val,
        'dimension': lambda v, m, val: len(v) == val,
        'metadata_equals': lambda v, m, val: m.get(val[0]) == val[1],
        'metadata_contains': lambda v, m, val: val[1] in str(m.get(val[0], '')),
        'metadata_range': lambda v, m, val: val[1] <= float(m.get(val[0], 0)) <= val[2],
    }
    return filter_functions.get(filter_name, lambda v, m, val: True)(vector, metadata, filter_value)