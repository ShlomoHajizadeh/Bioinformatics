import numpy as np


def random_unit_vector_3d(rng: np.random.Generator) -> np.ndarray:
    v = rng.normal(size=3)
    norm = np.linalg.norm(v)
    if norm == 0.0:
        return np.array([1.0, 0.0, 0.0], dtype=float)
    return v / norm


def safe_normalize(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm == 0.0:
        return np.zeros_like(v, dtype=float)
    return v / norm


def clip_norm(v: np.ndarray, max_norm: float) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm <= max_norm or norm == 0.0:
        return v
    return v * (max_norm / norm)