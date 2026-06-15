"""
Movement logic for bison and wolves with NEW RULES from PDF.
"""

import numpy as np
from config.config import GRASS_PREFERENCE_THRESHOLD


def move_wolves(wolves, grid, environment):
    """
    Move wolves randomly to neighboring cells.
    NEW RULE: Wolves cannot move to cells already occupied by other wolves.
    If all neighbors are occupied, wolf does not move.
    
    Args:
        wolves: List of Wolf objects
        grid: Grid object
        environment: Environment object
    """
    # Shuffle to avoid systematic bias
    shuffled_indices = np.random.permutation(len(wolves))
    
    for idx in shuffled_indices:
        wolf = wolves[idx]
        
        # Get current position
        old_x, old_y = grid.wrap_position(wolf.x, wolf.y)
        
        # Get neighboring positions
        neighbors = grid.get_von_neumann_neighbors(wolf.x, wolf.y)
        
        # Filter: Only cells without wolves
        free_neighbors = [
            (x, y) for x, y in neighbors
            if environment.get_wolf_count(x, y) == 0
        ]
        
        if len(free_neighbors) > 0:
            # Decrement old position
            environment.wolf_count[old_y, old_x] -= 1
            
            # Move to random free neighbor
            new_x, new_y = free_neighbors[np.random.randint(len(free_neighbors))]
            wolf.move_to(new_x, new_y)
            
            # Increment new position
            new_x_w, new_y_w = grid.wrap_position(new_x, new_y)
            environment.wolf_count[new_y_w, new_x_w] += 1
        # else: All neighbors occupied by wolves → no movement


def escape_bison_from_wolves(bison_list, grid, environment):
    """
    Phase 1: All bison in wolf-occupied cells escape SYNCHRONOUSLY.
    
    NEW RULE: If a wolf enters a cell occupied by bison, all bison will
    randomly move toward other cells that are not occupied by any wolf.
    
    Args:
        bison_list: List of Bison objects
        grid: Grid object
        environment: Environment object
        
    Returns:
        int: Number of bison that escaped
    """
    escape_list = []
    
    # Identify all bison that need to escape
    for bison in bison_list:
        x, y = grid.wrap_position(bison.x, bison.y)
        if environment.get_wolf_count(x, y) > 0:
            escape_list.append(bison)
    
    # Execute escapes synchronously
    escaped_count = 0
    
    for bison in escape_list:
        x_old, y_old = grid.wrap_position(bison.x, bison.y)
        
        # Find safe neighbors (grassland without wolves)
        neighbors = grid.get_von_neumann_neighbors(bison.x, bison.y)
        safe_neighbors = [
            (x, y) for x, y in neighbors
            if environment.is_grassland(x, y) and environment.get_wolf_count(x, y) == 0
        ]
        
        if len(safe_neighbors) > 0:
            # Decrement old position
            environment.bison_count[y_old, x_old] -= 1
            
            # Move to random safe neighbor
            new_x, new_y = safe_neighbors[np.random.randint(len(safe_neighbors))]
            bison.move_to(new_x, new_y)
            
            # Increment new position
            new_x_w, new_y_w = grid.wrap_position(new_x, new_y)
            environment.bison_count[new_y_w, new_x_w] += 1
            
            escaped_count += 1
        # else: No safe escape → stay put (trapped)
    
    return escaped_count


def move_bison_for_grazing(bison_list, grid, environment):
    """
    Phase 2: Bison move to better grazing grounds ASYNCHRONOUSLY.
    
    NEW RULES:
    - Bison move to better grazing if current stage < 4
    - Target: neighboring grassland with stage >= 4
    - If no such cell exists, move to next best
    - If all equal, move randomly
    - Cannot move to wolf-occupied cells
    
    Args:
        bison_list: List of Bison objects
        grid: Grid object
        environment: Environment object
        
    Returns:
        int: Number of bison that moved
    """
    # Asynchronous: random order
    shuffled_indices = np.random.permutation(len(bison_list))
    
    moved_count = 0
    
    for idx in shuffled_indices:
        bison = bison_list[idx]
        
        x_current, y_current = grid.wrap_position(bison.x, bison.y)
        
        # Skip if on forest (emergency - should not happen)
        if not environment.is_grassland(x_current, y_current):
            continue
        
        current_stage = environment.get_grass_stage(x_current, y_current)
        
        # Get neighbors
        neighbors = grid.get_von_neumann_neighbors(bison.x, bison.y)
        
        # Filter: grassland without wolves
        safe_neighbors = [
            (x, y) for x, y in neighbors
            if environment.is_grassland(x, y) and environment.get_wolf_count(x, y) == 0
        ]
        
        if len(safe_neighbors) == 0:
            continue  # No safe neighbors
        
        # RULE: If current stage < 4, prefer neighbors with stage >= 4
        if current_stage < GRASS_PREFERENCE_THRESHOLD:
            good_neighbors = [
                (x, y) for x, y in safe_neighbors
                if environment.get_grass_stage(x, y) >= GRASS_PREFERENCE_THRESHOLD
            ]
            
            if len(good_neighbors) > 0:
                # Move to random good neighbor
                target = good_neighbors[np.random.randint(len(good_neighbors))]
                
                # Execute move
                environment.bison_count[y_current, x_current] -= 1
                bison.move_to(target[0], target[1])
                target_x_w, target_y_w = grid.wrap_position(target[0], target[1])
                environment.bison_count[target_y_w, target_x_w] += 1
                
                moved_count += 1
                continue
        
        # FALLBACK: Move to next best (highest stage among neighbors)
        neighbor_stages = [
            (x, y, environment.get_grass_stage(x, y))
            for x, y in safe_neighbors
        ]
        
        max_stage = max(stage for _, _, stage in neighbor_stages)
        
        # Only move if neighbor is better than current
        if max_stage > current_stage:
            best_neighbors = [
                (x, y) for x, y, stage in neighbor_stages if stage == max_stage
            ]
            
            target = best_neighbors[np.random.randint(len(best_neighbors))]
            
            # Execute move
            environment.bison_count[y_current, x_current] -= 1
            bison.move_to(target[0], target[1])
            target_x_w, target_y_w = grid.wrap_position(target[0], target[1])
            environment.bison_count[target_y_w, target_x_w] += 1
            
            moved_count += 1
    
    return moved_count


def resolve_multi_occupancy(bison_list, grid, environment):
    """
    Phase 3: Resolve cells with >1 bison through ASYNCHRONOUS movement.
    
    NEW SOCIAL RULES:
    - If at end of time step a cell has >1 bison, random asynchronous movement starts
    - Last bison stays at the cell
    - Priority given to unoccupied neighboring cells
    - If none exist, move to cell with least number of bison
    - Break ties randomly
    
    Args:
        bison_list: List of Bison objects
        grid: Grid object
        environment: Environment object
        
    Returns:
        int: Number of resolution moves made
    """
    max_iterations = 100  # Prevent infinite loops
    total_moves = 0
    
    for iteration in range(max_iterations):
        # Find all overcrowded cells
        overcrowded_cells = []
        
        ny, nx = environment.grid.ny, environment.grid.nx
        for y in range(ny):
            for x in range(nx):
                if environment.bison_count[y, x] > 1:
                    overcrowded_cells.append((x, y))
        
        if len(overcrowded_cells) == 0:
            break  # All resolved
        
        # Process each overcrowded cell
        for x_cell, y_cell in overcrowded_cells:
            # Find all bison at this cell
            bison_here = [
                b for b in bison_list
                if grid.wrap_position(b.x, b.y) == (x_cell, y_cell)
            ]
            
            if len(bison_here) <= 1:
                continue  # Already resolved
            
            # Shuffle and move all except last
            np.random.shuffle(bison_here)
            
            for bison in bison_here[:-1]:  # All except last stay
                # Find neighbors
                neighbors = grid.get_von_neumann_neighbors(bison.x, bison.y)
                
                # Priority 1: Unoccupied grassland without wolves
                free_neighbors = [
                    (x, y) for x, y in neighbors
                    if environment.is_grassland(x, y)
                    and environment.get_wolf_count(x, y) == 0
                    and environment.get_bison_count(x, y) == 0
                ]
                
                if len(free_neighbors) > 0:
                    target = free_neighbors[np.random.randint(len(free_neighbors))]
                else:
                    # Priority 2: Least occupied neighbor
                    safe_neighbors = [
                        (x, y) for x, y in neighbors
                        if environment.is_grassland(x, y)
                        and environment.get_wolf_count(x, y) == 0
                    ]
                    
                    if len(safe_neighbors) == 0:
                        continue  # Cannot move - trapped
                    
                    # Find minimum occupancy
                    occupancies = [environment.get_bison_count(x, y) for x, y in safe_neighbors]
                    min_occ = min(occupancies)
                    
                    least_occupied = [
                        safe_neighbors[i] for i in range(len(safe_neighbors))
                        if occupancies[i] == min_occ
                    ]
                    
                    target = least_occupied[np.random.randint(len(least_occupied))]
                
                # Execute move
                environment.bison_count[y_cell, x_cell] -= 1
                bison.move_to(target[0], target[1])
                target_x_w, target_y_w = grid.wrap_position(target[0], target[1])
                environment.bison_count[target_y_w, target_x_w] += 1
                
                total_moves += 1
    
    return total_moves


def move_all_bison_new_protocol(bison_list, grid, environment):
    """
    Execute complete NEW 3-PHASE bison movement protocol:
    
    Phase 1: Wolf escape (synchronous)
    Phase 2: Grazing movement (asynchronous)
    Phase 3: Social resolution - dissolve multi-occupancy (asynchronous)
    
    Args:
        bison_list: List of Bison objects
        grid: Grid object
        environment: Environment object
        
    Returns:
        dict: Statistics about movements
    """
    stats = {}
    
    # PHASE 1: WOLF ESCAPE
    stats['escaped'] = escape_bison_from_wolves(bison_list, grid, environment)
    
    # PHASE 2: GRAZING MOVEMENT
    stats['grazed'] = move_bison_for_grazing(bison_list, grid, environment)
    
    # PHASE 3: SOCIAL RESOLUTION
    stats['resolved'] = resolve_multi_occupancy(bison_list, grid, environment)
    
    return stats