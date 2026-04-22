"""
Grid management for toroidal lattice with wrap-around boundaries.
"""

import numpy as np


class Grid:
    """
    Toroidal lattice grid with wrap-around indexing and neighborhood queries.
    """
    
    def __init__(self, nx, ny):
        """
        Initialize the grid.
        
        Args:
            nx: Grid width
            ny: Grid height
        """
        self.nx = nx
        self.ny = ny
    
    def wrap_position(self, x, y):
        """
        Wrap coordinates to handle toroidal boundaries.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            tuple: (wrapped_x, wrapped_y)
        """
        return x % self.nx, y % self.ny
    
    def position_to_index(self, x, y):
        """
        Convert (x, y) position to linear index.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            int: Linear index
        """
        x_wrapped, y_wrapped = self.wrap_position(x, y)
        return y_wrapped * self.nx + x_wrapped
    
    def index_to_position(self, index):
        """
        Convert linear index to (x, y) position.
        
        Args:
            index: Linear index
            
        Returns:
            tuple: (x, y) coordinates
        """
        y = index // self.nx
        x = index % self.nx
        return x, y
    
    def get_von_neumann_neighbors(self, x, y):
        """
        Get the 4 von Neumann neighbors (north, east, south, west).
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            list: List of (x, y) tuples for neighbors
        """
        neighbors = [
            (x, y - 1),  # North
            (x + 1, y),  # East
            (x, y + 1),  # South
            (x - 1, y),  # West
        ]
        
        # Wrap all neighbors
        return [self.wrap_position(nx, ny) for nx, ny in neighbors]
    
    def get_von_neumann_neighbor_indices(self, index):
        """
        Get von Neumann neighbor indices for a given cell index.
        
        Args:
            index: Linear cell index
            
        Returns:
            list: List of neighbor indices
        """
        x, y = self.index_to_position(index)
        neighbor_positions = self.get_von_neumann_neighbors(x, y)
        return [self.position_to_index(nx, ny) for nx, ny in neighbor_positions]
    
    def get_moore_neighbors(self, x, y):
        """
        Get the 8 Moore neighbors (including diagonals).
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            list: List of (x, y) tuples for neighbors
        """
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbors.append((x + dx, y + dy))
        
        # Wrap all neighbors
        return [self.wrap_position(nx, ny) for nx, ny in neighbors]
    
    def distance(self, x1, y1, x2, y2):
        """
        Calculate toroidal distance between two points.
        
        Args:
            x1, y1: First point coordinates
            x2, y2: Second point coordinates
            
        Returns:
            float: Toroidal distance
        """
        dx = min(abs(x2 - x1), self.nx - abs(x2 - x1))
        dy = min(abs(y2 - y1), self.ny - abs(y2 - y1))
        return np.sqrt(dx**2 + dy**2)
    
    def get_all_positions(self):
        """
        Get all valid grid positions.
        
        Returns:
            list: List of all (x, y) positions
        """
        positions = []
        for y in range(self.ny):
            for x in range(self.nx):
                positions.append((x, y))
        return positions
    
    def is_valid_position(self, x, y):
        """
        Check if position is valid (always True for toroidal grid after wrapping).
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            bool: Always True after wrapping
        """
        # After wrapping, all positions are valid
        return True