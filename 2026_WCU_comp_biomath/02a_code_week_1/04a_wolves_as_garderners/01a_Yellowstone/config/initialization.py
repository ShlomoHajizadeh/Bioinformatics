"""
Initialization routines for environment setup.
"""

import numpy as np
from config.config import (
    NX, NY, 
    CELL_TYPE_GRASS, CELL_TYPE_FOREST,
    INITIAL_FOREST_FRACTION,
    INITIAL_GRASS_STAGE_MEAN,
    INITIAL_GRASS_STAGE_STD,
    MIN_GRASS_STAGE,
    MAX_GRASS_STAGE
)


def initialize_environment(random_seed=None, nx=None, ny=None):
    """
    Initialize the environment with random forest placement and grass stages.
    
    Args:
        random_seed: Random seed for reproducibility
        nx: Grid width (uses config.NX if None)
        ny: Grid height (uses config.NY if None)
        
    Returns:
        tuple: (cell_types, grass_stages, stage5_counter)
    """
    # Use default dimensions if not provided
    if nx is None:
        nx = NX
    if ny is None:
        ny = NY
    
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Initialize all cells as grassland
    cell_types = np.full((ny, nx), CELL_TYPE_GRASS, dtype='U6')
    
    # Randomly assign forest cells
    n_total_cells = nx * ny
    n_forest_cells = int(n_total_cells * INITIAL_FOREST_FRACTION)
    
    # Get random positions for forest
    all_positions = [(x, y) for y in range(ny) for x in range(nx)]
    forest_positions = np.random.choice(len(all_positions), n_forest_cells, replace=False)
    
    for idx in forest_positions:
        x, y = all_positions[idx]
        cell_types[y, x] = CELL_TYPE_FOREST
    
    # Initialize grass stages for grassland cells (0-10 scale)
    grass_stages = np.zeros((ny, nx), dtype=int)
    
    for y in range(ny):
        for x in range(nx):
            if cell_types[y, x] == CELL_TYPE_GRASS:
                # Sample from normal distribution, clipped to [0, 10]
                stage = np.random.normal(INITIAL_GRASS_STAGE_MEAN, INITIAL_GRASS_STAGE_STD)
                stage = int(np.clip(stage, MIN_GRASS_STAGE, MAX_GRASS_STAGE))
                grass_stages[y, x] = stage
    
    # Initialize stage5_counter (now stage10_counter - all zeros initially)
    stage5_counter = np.zeros((ny, nx), dtype=int)
    
    return cell_types, grass_stages, stage5_counter