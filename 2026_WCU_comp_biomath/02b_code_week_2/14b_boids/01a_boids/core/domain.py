"""
Domain and boundary conditions for Reynolds boids simulation.
"""
import numpy as np


class Domain:
    """
    Represents the simulation domain with periodic boundary conditions.
    
    Attributes:
        size: array of domain dimensions
        dimension: spatial dimension (2 or 3)
    """
    
    def __init__(self, size):
        """
        Initialize domain.
        
        Args:
            size: tuple or array of domain dimensions (Lx, Ly) or (Lx, Ly, Lz)
        """
        self.size = np.array(size, dtype=float)
        self.dimension = len(self.size)
        
    def wrap(self, positions):
        """
        Apply periodic boundary conditions to positions.
        
        Args:
            positions: (n_agents, dimension) array of positions
            
        Returns:
            ndarray: wrapped positions
        """
        return np.mod(positions, self.size)
    
    def minimum_image(self, delta):
        """
        Apply minimum image convention for distance calculations.
        
        For periodic boundaries, finds the shortest distance between points
        accounting for wrapping.
        
        Args:
            delta: displacement vector(s), shape (dimension,) or (n, dimension)
            
        Returns:
            ndarray: corrected displacement using minimum image convention
        """
        # Handle both single vector and array of vectors
        delta = np.asarray(delta)
        
        # Wrap delta to [-L/2, L/2] for each dimension
        delta = delta - self.size * np.round(delta / self.size)
        
        return delta
    
    def distance(self, pos1, pos2):
        """
        Compute distance between two positions with periodic boundaries.
        
        Args:
            pos1: position 1
            pos2: position 2
            
        Returns:
            float: distance
        """
        delta = self.minimum_image(pos1 - pos2)
        return np.linalg.norm(delta)
    
    def get_bounds(self):
        """
        Get domain bounds.
        
        Returns:
            tuple: (lower_bounds, upper_bounds)
        """
        lower = np.zeros(self.dimension)
        upper = self.size.copy()
        return lower, upper