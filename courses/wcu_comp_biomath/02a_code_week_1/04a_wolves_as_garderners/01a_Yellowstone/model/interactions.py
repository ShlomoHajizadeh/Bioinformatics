"""
Interaction detection between agents.
"""

import numpy as np


def detect_wolf_bison_encounters(bison_list, wolves, grid, environment):
    """
    Detect and count cells where wolves and bison are present simultaneously.
    
    Args:
        bison_list: List of Bison objects
        wolves: List of Wolf objects
        grid: Grid object
        environment: Environment object
        
    Returns:
        int: Number of cells with wolf-bison encounters
    """
    encounter_cells = set()
    
    # Check each bison position
    for bison in bison_list:
        x, y = grid.wrap_position(bison.x, bison.y)
        
        # Check if there's a wolf at this position
        if environment.get_wolf_count(x, y) > 0:
            encounter_cells.add((x, y))
    
    return len(encounter_cells)


def get_encounter_positions(bison_list, wolves, grid, environment):
    """
    Get all positions where wolves and bison encounter each other.
    
    Args:
        bison_list: List of Bison objects
        wolves: List of Wolf objects
        grid: Grid object
        environment: Environment object
        
    Returns:
        list: List of (x, y) tuples where encounters occur
    """
    encounter_cells = set()
    
    for bison in bison_list:
        x, y = grid.wrap_position(bison.x, bison.y)
        
        if environment.get_wolf_count(x, y) > 0:
            encounter_cells.add((x, y))
    
    return list(encounter_cells)


def count_bison_in_danger(bison_list, grid, environment):
    """
    Count how many bison are currently in cells with wolves.
    
    Args:
        bison_list: List of Bison objects
        grid: Grid object
        environment: Environment object
        
    Returns:
        int: Number of bison in wolf-occupied cells
    """
    count = 0
    
    for bison in bison_list:
        x, y = grid.wrap_position(bison.x, bison.y)
        
        if environment.get_wolf_count(x, y) > 0:
            count += 1
    
    return count