"""
Update rules for grass stages and forest conversion (NEW SIMPLIFIED RULES).
"""

import numpy as np
from config.config import (
    CELL_TYPE_GRASS, CELL_TYPE_FOREST,
    MIN_GRASS_STAGE, MAX_GRASS_STAGE,
    GRASS_CHANGE_GRAZING,
    GRASS_CHANGE_RECOVERY,
    STAGE10_THRESHOLD
)


def update_grass_stages(environment):
    """
    Update grass stages based on NEW SIMPLIFIED rules:
    - Change -1: >= 1 bison in cell
    - Change +1: 0 bison in cell
    
    Args:
        environment: Environment object
        
    Returns:
        dict: Statistics about changes
    """
    ny, nx = environment.grid.ny, environment.grid.nx
    
    changes = {
        'grazed': 0,
        'recovered': 0,
        'unchanged_forest': 0
    }
    
    for y in range(ny):
        for x in range(nx):
            # Only update grassland cells
            if environment.cell_types[y, x] != CELL_TYPE_GRASS:
                changes['unchanged_forest'] += 1
                continue
            
            # Get bison count
            n_bison = environment.bison_count[y, x]
            current_stage = environment.grass_stages[y, x]
            
            # SIMPLIFIED: Only two cases
            if n_bison >= 1:
                change = GRASS_CHANGE_GRAZING  # -1
                changes['grazed'] += 1
            else:
                change = GRASS_CHANGE_RECOVERY  # +1
                changes['recovered'] += 1
            
            # Apply change with bounds
            new_stage = np.clip(current_stage + change, MIN_GRASS_STAGE, MAX_GRASS_STAGE)
            environment.grass_stages[y, x] = new_stage
    
    return changes


def update_stage10_counters(environment):
    """
    Update counters for cells at stage 10.
    Increment counter if at stage 10, reset otherwise.
    
    Args:
        environment: Environment object
    """
    ny, nx = environment.grid.ny, environment.grid.nx
    
    for y in range(ny):
        for x in range(nx):
            # Only for grassland cells
            if environment.cell_types[y, x] != CELL_TYPE_GRASS:
                continue
            
            if environment.grass_stages[y, x] == MAX_GRASS_STAGE:
                # Increment counter
                environment.stage5_counter[y, x] += 1
            else:
                # Reset counter
                environment.stage5_counter[y, x] = 0


def convert_to_forest(environment):
    """
    Convert grassland cells to forest if they have been at stage 10
    for STAGE10_THRESHOLD consecutive steps.
    
    Args:
        environment: Environment object
        
    Returns:
        int: Number of cells converted to forest
    """
    ny, nx = environment.grid.ny, environment.grid.nx
    conversions = 0
    
    for y in range(ny):
        for x in range(nx):
            # Only grassland cells can convert
            if environment.cell_types[y, x] != CELL_TYPE_GRASS:
                continue
            
            # Check if threshold reached
            if environment.stage5_counter[y, x] >= STAGE10_THRESHOLD:
                # Convert to forest
                environment.cell_types[y, x] = CELL_TYPE_FOREST
                environment.grass_stages[y, x] = 0  # Forest has no grass stage
                environment.stage5_counter[y, x] = 0  # Reset counter
                conversions += 1
    
    return conversions


def apply_all_updates(environment):
    """
    Apply all update rules in correct order:
    1. Update grass stages based on grazing
    2. Update stage 10 counters
    3. Convert eligible cells to forest
    
    Args:
        environment: Environment object
        
    Returns:
        dict: Combined statistics from all updates
    """
    # Step 1: Update grass stages
    grass_changes = update_grass_stages(environment)
    
    # Step 2: Update stage 10 counters
    update_stage10_counters(environment)
    
    # Step 3: Convert to forest
    forest_conversions = convert_to_forest(environment)
    
    # Combine statistics
    stats = {
        'grazed': grass_changes['grazed'],
        'recovered': grass_changes['recovered'],
        'forest_conversions': forest_conversions
    }
    
    return stats