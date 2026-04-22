"""Neighborhood detection with periodic boundary conditions."""
import numpy as np
from config import VicsekConfig


def periodic_distance(pos1: np.ndarray, pos2: np.ndarray, L: float) -> np.ndarray:
    """Compute periodic distance on a toroidal domain.
    
    Args:
        pos1: Positions of shape (N, 2) or (2,)
        pos2: Positions of shape (M, 2) or (2,)
        L: Domain size
        
    Returns:
        distances: Euclidean distances with periodic boundary conditions
    """
    delta = np.abs(pos1 - pos2)
    delta = np.minimum(delta, L - delta)
    return np.linalg.norm(delta, axis=-1)


def periodic_displacement(pos1: np.ndarray, pos2: np.ndarray, L: float) -> np.ndarray:
    """Compute periodic displacement vector on a toroidal domain.
    
    Args:
        pos1: Positions of shape (N, 2)
        pos2: Positions of shape (M, 2)
        L: Domain size
        
    Returns:
        displacements: Displacement vectors with periodic boundary conditions
    """
    delta = pos2 - pos1
    delta = np.where(delta > L/2, delta - L, delta)
    delta = np.where(delta < -L/2, delta + L, delta)
    return delta


def find_neighbors(positions: np.ndarray, config: VicsekConfig) -> list[np.ndarray]:
    """Find neighbors within interaction radius for all particles.
    
    Args:
        positions: Array of shape (N, 2) with particle positions
        config: Vicsek configuration parameters
        
    Returns:
        neighbors: List of N arrays, where neighbors[i] contains indices 
                   of particles within radius r of particle i (including i itself)
    """
    N = config.N
    L = config.L
    r = config.r
    
    neighbors = []
    
    for i in range(N):
        # Compute distances to all other particles
        distances = periodic_distance(positions[i], positions, L)
        # Find indices within interaction radius (including self)
        neighbor_indices = np.where(distances <= r)[0]
        neighbors.append(neighbor_indices)
    
    return neighbors


def compute_distance_matrix(positions: np.ndarray, L: float) -> np.ndarray:
    """Compute pairwise distance matrix with periodic boundaries.
    
    Args:
        positions: Array of shape (N, 2) with particle positions
        L: Domain size
        
    Returns:
        dist_matrix: Array of shape (N, N) with pairwise distances
    """
    N = positions.shape[0]
    dist_matrix = np.zeros((N, N))
    
    for i in range(N):
        dist_matrix[i] = periodic_distance(positions[i], positions, L)
    
    return dist_matrix