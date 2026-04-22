"""
Domain handling with periodic boundary conditions.
"""
import numpy as np


class Domain:
    """
    Represents the simulation domain with periodic boundary conditions.
    """
    
    def __init__(self, size):
        """
        Initialize domain.
        
        Args:
            size: tuple of domain dimensions (Lx, Ly) or (Lx, Ly, Lz)
        """
        self.size = np.array(size, dtype=float)
        self.dimension = len(size)
    
    def wrap(self, positions):
        """
        Apply periodic boundary conditions to positions.
        
        Args:
            positions: array of positions
            
        Returns:
            wrapped positions
        """
        return positions % self.size
    
    def minimum_image(self, vector):
        """
        Apply minimum image convention to a single vector.
        
        Args:
            vector: displacement vector
            
        Returns:
            minimum image vector
        """
        # Wrap to [-L/2, L/2]
        half_size = self.size / 2
        vector = vector - self.size * np.round(vector / self.size)
        return vector
    
    def minimum_image_array(self, vectors):
        """
        Apply minimum image convention to an array of vectors.
        
        Args:
            vectors: array of displacement vectors (N, dimension)
            
        Returns:
            minimum image vectors
        """
        # Wrap to [-L/2, L/2]
        half_size = self.size / 2
        vectors = vectors - self.size * np.round(vectors / self.size)
        return vectors
    
    def distance(self, pos1, pos2):
        """
        Compute minimum image distance between two positions.
        
        Args:
            pos1: first position
            pos2: second position
            
        Returns:
            minimum image distance
        """
        diff = pos1 - pos2
        diff = self.minimum_image(diff)
        return np.linalg.norm(diff)
    
    def distance_matrix(self, positions):
        """
        Compute pairwise distance matrix with periodic boundaries.
        
        Args:
            positions: array of positions (N, dimension)
            
        Returns:
            distance matrix (N, N)
        """
        n = len(positions)
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                d = self.distance(positions[i], positions[j])
                distances[i, j] = d
                distances[j, i] = d
        
        return distances
    
    def get_box_indices(self, positions, box_size):
        """
        Assign positions to grid boxes for efficient neighbor finding.
        
        Args:
            positions: array of positions
            box_size: size of each box
            
        Returns:
            array of box indices for each position
        """
        n_boxes_per_dim = np.ceil(self.size / box_size).astype(int)
        box_indices = np.floor(positions / box_size).astype(int)
        
        # Handle periodic boundaries
        box_indices = box_indices % n_boxes_per_dim
        
        # Convert multi-dimensional index to single index
        if self.dimension == 2:
            flat_indices = box_indices[:, 0] * n_boxes_per_dim[1] + box_indices[:, 1]
        elif self.dimension == 3:
            flat_indices = (box_indices[:, 0] * n_boxes_per_dim[1] * n_boxes_per_dim[2] +
                          box_indices[:, 1] * n_boxes_per_dim[2] +
                          box_indices[:, 2])
        else:
            raise ValueError(f"Unsupported dimension: {self.dimension}")
        
        return flat_indices, n_boxes_per_dim