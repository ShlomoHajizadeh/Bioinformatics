"""
Environment management: cell types, grass stages, and occupancy tracking.
"""

import numpy as np
from config.config import (
    CELL_TYPE_GRASS, CELL_TYPE_FOREST,
    MIN_GRASS_STAGE, MAX_GRASS_STAGE
)


class Environment:
    """
    Manages the spatial environment including cell types, grass stages, and agent occupancy.
    """
    
    def __init__(self, grid, cell_types, grass_stages, stage5_counter):
        """
        Initialize environment.
        
        Args:
            grid: Grid object
            cell_types: 2D array of cell types
            grass_stages: 2D array of grass stages (0-10)
            stage5_counter: 2D array counting consecutive steps at stage 10
        """
        self.grid = grid
        self.cell_types = cell_types
        self.grass_stages = grass_stages
        self.stage5_counter = stage5_counter
        
        # Initialize occupancy tracking
        self.bison_count = np.zeros((grid.ny, grid.nx), dtype=int)
        self.wolf_count = np.zeros((grid.ny, grid.nx), dtype=int)
    
    def is_grassland(self, x, y):
        """
        Check if a cell is grassland.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            bool: True if grassland, False otherwise
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        return self.cell_types[y_wrapped, x_wrapped] == CELL_TYPE_GRASS
    
    def is_forest(self, x, y):
        """
        Check if a cell is forest.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            bool: True if forest, False otherwise
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        return self.cell_types[y_wrapped, x_wrapped] == CELL_TYPE_FOREST
    
    def get_grass_stage(self, x, y):
        """
        Get grass stage at a cell.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            int: Grass stage (0-10, or 0 for forest)
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        return self.grass_stages[y_wrapped, x_wrapped]
    
    def set_grass_stage(self, x, y, stage):
        """
        Set grass stage at a cell.
        
        Args:
            x, y: Cell coordinates
            stage: New grass stage (0-10)
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        self.grass_stages[y_wrapped, x_wrapped] = np.clip(stage, MIN_GRASS_STAGE, MAX_GRASS_STAGE)
    
    def get_bison_count(self, x, y):
        """
        Get number of bison at a cell.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            int: Number of bison
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        return self.bison_count[y_wrapped, x_wrapped]
    
    def get_wolf_count(self, x, y):
        """
        Get number of wolves at a cell.
        
        Args:
            x, y: Cell coordinates
            
        Returns:
            int: Number of wolves
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        return self.wolf_count[y_wrapped, x_wrapped]
    
    def increment_bison_count(self, x, y):
        """
        Increment bison count at a cell.
        
        Args:
            x, y: Cell coordinates
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        self.bison_count[y_wrapped, x_wrapped] += 1
    
    def increment_wolf_count(self, x, y):
        """
        Increment wolf count at a cell.
        
        Args:
            x, y: Cell coordinates
        """
        x_wrapped, y_wrapped = self.grid.wrap_position(x, y)
        self.wolf_count[y_wrapped, x_wrapped] += 1
    
    def reset_occupancy(self):
        """
        Reset all occupancy counts to zero.
        """
        self.bison_count.fill(0)
        self.wolf_count.fill(0)
    
    def get_state_summary(self):
        """
        Get summary statistics of current environment state.
        
        Returns:
            dict: Summary statistics
        """
        total_forest = np.sum(self.cell_types == CELL_TYPE_FOREST)
        total_grassland = np.sum(self.cell_types == CELL_TYPE_GRASS)
        
        # Calculate mean grass stage (only for grassland cells)
        grassland_mask = self.cell_types == CELL_TYPE_GRASS
        if np.any(grassland_mask):
            mean_grass_stage = np.mean(self.grass_stages[grassland_mask])
        else:
            mean_grass_stage = 0.0
        
        # Count overgrazed cells (stage 0)
        overgrazed_cells = np.sum((self.cell_types == CELL_TYPE_GRASS) & (self.grass_stages == 0))
        
        # Count cells at stage 10 (emerging forest)
        stage10_cells = np.sum((self.cell_types == CELL_TYPE_GRASS) & (self.grass_stages == MAX_GRASS_STAGE))
        
        return {
            'total_forest': total_forest,
            'total_grassland': total_grassland,
            'mean_grass_stage': mean_grass_stage,
            'overgrazed_cells': overgrazed_cells,
            'stage10_cells': stage10_cells
        }