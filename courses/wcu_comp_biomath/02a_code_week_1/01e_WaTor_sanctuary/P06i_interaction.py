#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

import numpy as np
from P06i_helpers import is_in_sanctuary, get_direction_move
from P06i_neighbors import (find_movement_neighbors, find_breeding_neighbors, 
                            find_fish_neighbors, find_fish_neighbors_8)

def simulate_fish_step(N, fish, fish_breeding_time):
    """
    Simulates one step of the fish simulation, including movement and breeding.
    """
    # Create the grid to store occupied cells
    grid = [[0 for _ in range(N)] for _ in range(N)]
    for x, y, _, _ in fish:
        grid[y][x] = 1

    new_fish = []
    for x, y, direction, age in fish:
        # Move the fish
        movement_neighbors = find_movement_neighbors(grid, x, y, N)
        if movement_neighbors:
            new_x, new_y = movement_neighbors[np.random.randint(0, len(movement_neighbors))]
            new_fish.append((new_x, new_y, direction, age + 1))
            grid[new_y][new_x] = 1
            grid[y][x] = 0
        else:
            new_fish.append((x, y, direction, age + 1))

    # Update the grid after the movement
    grid = [[0 for _ in range(N)] for _ in range(N)]
    for x, y, _, _ in new_fish:
        grid[y][x] = 1

    # Breed the fish
    final_fish = []
    offspring = []
    for x, y, direction, age in new_fish:
        if (age-1) >= fish_breeding_time:
            breeding_neighbors = find_breeding_neighbors(grid, x, y, N, exclude_sanctuary=False)
            if breeding_neighbors:
                new_x, new_y = breeding_neighbors[np.random.randint(0, len(breeding_neighbors))]
                final_fish.append((x, y, direction, 0))
                offspring.append((new_x, new_y, direction, 0))
                grid[new_y][new_x] = 1
            else:
                final_fish.append((x, y, direction, age))
        else:
            final_fish.append((x, y, direction, age))

    return final_fish + offspring

def simulate_predator_step(N, fish, sharks, hunters, shark_breeding_time, shark_starving_time, 
                          hunter_breeding_time, hunter_starving_time, breeding_energy):
    """
    Simulates one step for both sharks and hunters together to handle conflicts.
    HARD SANCTUARY: Predators cannot enter (blocked like a net).
    """
    # DEBUG: Check initial predator positions
    print("\n=== PREDATOR STEP START ===")
    sharks_in_sanctuary = [(x, y) for x, y, _, _, _, _ in sharks if is_in_sanctuary(x, y, N)]
    hunters_in_sanctuary = [(x, y) for x, y, _, _, _, _ in hunters if is_in_sanctuary(x, y, N)]
    if sharks_in_sanctuary:
        print(f"DEBUG: Sharks ALREADY in sanctuary at start: {sharks_in_sanctuary}")
    if hunters_in_sanctuary:
        print(f"DEBUG: Hunters ALREADY in sanctuary at start: {hunters_in_sanctuary}")
    
    # Create grids
    fish_grid = [[0 for _ in range(N)] for _ in range(N)]
    predator_grid = [[0 for _ in range(N)] for _ in range(N)]
    fish_dict = {}
    
    for x, y, _, age in fish:
        fish_grid[y][x] = 1
        fish_dict[(x, y)] = age
    
    for x, y, _, _, _, _ in sharks:
        predator_grid[y][x] = 1
    for x, y, _, _, _, _ in hunters:
        predator_grid[y][x] = 1

    eaten_fish = set()
    
    # HUNTERS MOVE FIRST
    print("\n--- Processing Hunters ---")
    new_hunters = process_hunters(hunters, fish_grid, predator_grid, fish_dict, eaten_fish, N)
    
    # Update fish list after hunters
    remaining_fish = [(x, y, d, a) for x, y, d, a in fish if (x, y) not in eaten_fish]
    fish_dict = {(x, y): age for x, y, _, age in remaining_fish}
    
    # SHARKS MOVE SECOND
    print("\n--- Processing Sharks ---")
    new_sharks = process_sharks(sharks, fish_grid, predator_grid, fish_dict, eaten_fish, N)
    
    # Remove all eaten fish
    remaining_fish = [(x, y, d, a) for x, y, d, a in remaining_fish if (x, y) not in eaten_fish]

    # Remove starved predators
    surviving_sharks = [(x, y, d, a, st, rl) for x, y, d, a, st, rl in new_sharks 
                        if st < shark_starving_time and rl >= 0]
    surviving_hunters = [(x, y, d, a, st, rl) for x, y, d, a, st, rl in new_hunters 
                         if st < hunter_starving_time and rl >= 0]

    # DEBUG: Check after movement
    sharks_in_sanctuary = [(x, y) for x, y, _, _, _, _ in surviving_sharks if is_in_sanctuary(x, y, N)]
    hunters_in_sanctuary = [(x, y) for x, y, _, _, _, _ in surviving_hunters if is_in_sanctuary(x, y, N)]
    if sharks_in_sanctuary:
        print(f"DEBUG: Sharks in sanctuary AFTER movement: {sharks_in_sanctuary}")
    if hunters_in_sanctuary:
        print(f"DEBUG: Hunters in sanctuary AFTER movement: {hunters_in_sanctuary}")

    # Update predator grid
    predator_grid = [[0 for _ in range(N)] for _ in range(N)]
    for x, y, _, _, _, _ in surviving_sharks:
        predator_grid[y][x] = 1
    for x, y, _, _, _, _ in surviving_hunters:
        predator_grid[y][x] = 1

    # Breed sharks
    print("\n--- Breeding Sharks ---")
    final_sharks = breed_predators(surviving_sharks, predator_grid, N, 
                                   shark_breeding_time, breeding_energy, "shark")
    
    # Breed hunters
    print("\n--- Breeding Hunters ---")
    final_hunters = breed_predators(surviving_hunters, predator_grid, N, 
                                    hunter_breeding_time, breeding_energy, "hunter")

    # DEBUG: Check final positions
    sharks_in_sanctuary = [(x, y) for x, y, _, _, _, _ in final_sharks if is_in_sanctuary(x, y, N)]
    hunters_in_sanctuary = [(x, y) for x, y, _, _, _, _ in final_hunters if is_in_sanctuary(x, y, N)]
    if sharks_in_sanctuary:
        print(f"DEBUG: Sharks in sanctuary AFTER breeding: {sharks_in_sanctuary}")
    if hunters_in_sanctuary:
        print(f"DEBUG: Hunters in sanctuary AFTER breeding: {hunters_in_sanctuary}")
    print("=== PREDATOR STEP END ===\n")

    return remaining_fish, final_sharks, final_hunters

def process_hunters(hunters, fish_grid, predator_grid, fish_dict, eaten_fish, N):
    """Process hunter movement and hunting. CANNOT enter sanctuary (blocked by net)."""
    new_hunters = []
    
    for x, y, direction, age, starve_time, resource_level in hunters:
        # Check if hunter is already in sanctuary (should never happen)
        if is_in_sanctuary(x, y, N):
            print(f"  ⚠️ WARNING: Hunter ALREADY in sanctuary at ({x}, {y}) - REMOVING")
            continue
            
        fish_pos = find_fish_neighbors_8(fish_grid, x, y, N, exclude_sanctuary=True)
        
        # Check if fish position is valid (not eaten and NOT in sanctuary)
        if fish_pos and fish_pos not in eaten_fish:
            new_x, new_y = fish_pos
            # Double-check target is not in sanctuary
            if is_in_sanctuary(new_x, new_y, N):
                print(f"  ❌ ERROR: Hunter at ({x},{y}) TRIED to eat sanctuary fish at ({new_x},{new_y})")
                # Stay in place instead
                new_hunters.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))
            else:
                # Valid move - eat the fish
                fish_age = fish_dict[(new_x, new_y)]
                new_hunters.append((new_x, new_y, direction, age + 1, 0, resource_level + fish_age))
                eaten_fish.add((new_x, new_y))
                predator_grid[new_y][new_x] = 1
                predator_grid[y][x] = 0
                fish_grid[new_y][new_x] = 0
        else:
            # No fish nearby, move in direction (with sanctuary check)
            new_x, new_y = get_direction_move(x, y, direction, N, check_sanctuary=True)
            
            # Verify new position is not in sanctuary
            if is_in_sanctuary(new_x, new_y, N):
                print(f"  ❌ ERROR: Hunter TRIED to move from ({x},{y}) to sanctuary ({new_x},{new_y}) via direction {direction}")
                # Stay in place
                new_hunters.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))
            elif (predator_grid[new_y][new_x] == 0 and fish_grid[new_y][new_x] == 0):
                # Valid move
                new_hunters.append((new_x, new_y, direction, age + 1, starve_time + 1, resource_level - 1))
                predator_grid[new_y][new_x] = 1
                predator_grid[y][x] = 0
            else:
                # Cell occupied, stay in place
                new_hunters.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))
    
    return new_hunters

def process_sharks(sharks, fish_grid, predator_grid, fish_dict, eaten_fish, N):
    """Process shark movement and hunting. CANNOT enter sanctuary (blocked by net)."""
    new_sharks = []
    
    for x, y, direction, age, starve_time, resource_level in sharks:
        # Check if shark is already in sanctuary (should never happen)
        if is_in_sanctuary(x, y, N):
            print(f"  ⚠️ WARNING: Shark ALREADY in sanctuary at ({x}, {y}) - REMOVING")
            continue
            
        fish_neighbors = find_fish_neighbors(fish_grid, x, y, N, exclude_sanctuary=True)
        # Filter out already eaten fish
        fish_neighbors = [pos for pos in fish_neighbors if pos not in eaten_fish]
        
        if fish_neighbors:
            new_x, new_y = fish_neighbors[np.random.randint(0, len(fish_neighbors))]
            # Double-check target is not in sanctuary
            if is_in_sanctuary(new_x, new_y, N):
                print(f"  ❌ ERROR: Shark at ({x},{y}) TRIED to eat sanctuary fish at ({new_x},{new_y})")
                # Stay in place
                new_sharks.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))
            else:
                # Valid move - eat the fish
                fish_age = fish_dict[(new_x, new_y)]
                new_sharks.append((new_x, new_y, direction, age + 1, 0, resource_level + fish_age))
                eaten_fish.add((new_x, new_y))
                predator_grid[new_y][new_x] = 1
                predator_grid[y][x] = 0
                fish_grid[new_y][new_x] = 0
        else:
            # No fish nearby, move in direction (with sanctuary check)
            new_x, new_y = get_direction_move(x, y, direction, N, check_sanctuary=True)
            
            # Verify new position is not in sanctuary
            if is_in_sanctuary(new_x, new_y, N):
                print(f"  ❌ ERROR: Shark TRIED to move from ({x},{y}) to sanctuary ({new_x},{new_y}) via direction {direction}")
                # Stay in place
                new_sharks.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))
            elif (predator_grid[new_y][new_x] == 0 and fish_grid[new_y][new_x] == 0):
                # Valid move
                new_sharks.append((new_x, new_y, direction, age + 1, starve_time + 1, resource_level - 1))
                predator_grid[new_y][new_x] = 1
                predator_grid[y][x] = 0
            else:
                # Cell occupied, stay in place
                new_sharks.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))
    
    return new_sharks

def breed_predators(predators, predator_grid, N, breeding_time, breeding_energy, species="predator"):
    """Breed predators (sharks or hunters). CANNOT breed into sanctuary."""
    final_predators = []
    offspring = []
    
    for x, y, direction, age, starve_time, resource_level in predators:
        # Check if parent is in sanctuary (should never happen)
        if is_in_sanctuary(x, y, N):
            print(f"  ⚠️ WARNING: {species} parent in sanctuary at ({x}, {y}) - REMOVING")
            continue
            
        if (age - 1) >= breeding_time and resource_level > breeding_energy:
            breeding_neighbors = find_breeding_neighbors(predator_grid, x, y, N, exclude_sanctuary=True)
            if breeding_neighbors:
                new_x, new_y = breeding_neighbors[np.random.randint(0, len(breeding_neighbors))]
                # Double-check offspring position is not in sanctuary
                if is_in_sanctuary(new_x, new_y, N):
                    print(f"  ❌ ERROR: {species} TRIED to breed into sanctuary at ({new_x},{new_y}) from ({x},{y})")
                    # Don't breed, keep parent with original age
                    final_predators.append((x, y, direction, age, starve_time, resource_level))
                else:
                    # Valid breeding
                    parent_resource = resource_level // 2
                    child_resource = resource_level - parent_resource
                    final_predators.append((x, y, direction, 0, starve_time, parent_resource))
                    offspring.append((new_x, new_y, direction, 0, 0, child_resource))
                    predator_grid[new_y][new_x] = 1
            else:
                # No breeding neighbors available
                final_predators.append((x, y, direction, age, starve_time, resource_level))
        else:
            # Not ready to breed or not enough resources
            final_predators.append((x, y, direction, age, starve_time, resource_level))
    
    return final_predators + offspring

def simulate_step(N, fish, sharks, hunters, fish_breeding_time, shark_breeding_time, shark_starving_time,
                 hunter_breeding_time, hunter_starving_time, breeding_energy):
    """
    Simulates one complete step of the Wa-Tor world.
    """
    # Fish move and breed first
    fish = simulate_fish_step(N, fish, fish_breeding_time)
    
    # Then predators move, hunt, and breed
    fish, sharks, hunters = simulate_predator_step(N, fish, sharks, hunters, 
                                                   shark_breeding_time, shark_starving_time,
                                                   hunter_breeding_time, hunter_starving_time, 
                                                   breeding_energy)
    
    return fish, sharks, hunters