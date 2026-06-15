#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

import numpy as np

def find_movement_neighbors(grid, x, y, N):
    """
    Find the unoccupied neighboring cells for movement.
    """
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if grid[new_y][new_x] == 0:
            neighbors.append((new_x, new_y))
    return neighbors

def find_breeding_neighbors(grid, x, y, N):
    """
    Find the unoccupied neighboring cells for breeding.
    """
    neighbors = []
    for dx, dy in [(0, 1), (-1, 1), (1, 1), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if grid[new_y][new_x] == 0:
            neighbors.append((new_x, new_y))
    return neighbors

def find_fish_neighbors(fish_grid, x, y, N):
    """
    Find neighboring cells (4 directions) that contain fish.
    """
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if fish_grid[new_y][new_x] == 1:
            neighbors.append((new_x, new_y))
    return neighbors

def find_fish_neighbors_8(fish_grid, x, y, N):
    """
    Find neighboring cells (8 directions) that contain fish.
    Returns the first fish found in the order checked.
    """
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if fish_grid[new_y][new_x] == 1:
            return (new_x, new_y)
    return None

def get_direction_move(x, y, direction, N):
    """
    Get the new position based on current position and direction.
    Direction: 1=North, 2=East, 3=South, 4=West
    """
    if direction == 1:  # North
        return x, (y + 1) % N
    elif direction == 2:  # East
        return (x + 1) % N, y
    elif direction == 3:  # South
        return x, (y - 1) % N
    else:  # direction == 4, West
        return (x - 1) % N, y

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
        # we updated the age during the movement
        if (age-1) >= fish_breeding_time:
            breeding_neighbors = find_breeding_neighbors(grid, x, y, N)
            if breeding_neighbors:
                new_x, new_y = breeding_neighbors[np.random.randint(0, len(breeding_neighbors))]
                final_fish.append((x, y, direction, 0))  # Parent with age reset to 0
                offspring.append((new_x, new_y, direction, 0))  # Offspring with age 0
                grid[new_y][new_x] = 1
            else:
                final_fish.append((x, y, direction, age))  # Parent keeps its age if can't breed
        else:
            final_fish.append((x, y, direction, age))  # Fish not old enough to breed

    return final_fish + offspring

def simulate_predator_step(N, fish, sharks, hunters, shark_breeding_time, shark_starving_time, 
                          hunter_breeding_time, hunter_starving_time, breeding_energy):
    """
    Simulates one step for both sharks and hunters together to handle conflicts.
    Hunters move first, then sharks.
    """
    # Create grids to track fish and predator positions
    fish_grid = [[0 for _ in range(N)] for _ in range(N)]
    predator_grid = [[0 for _ in range(N)] for _ in range(N)]  # Combined predator grid
    fish_dict = {}  # Maps (x, y) to fish age
    
    for x, y, _, age in fish:
        fish_grid[y][x] = 1
        fish_dict[(x, y)] = age
    
    # Mark all predator positions
    for x, y, _, _, _, _ in sharks:
        predator_grid[y][x] = 1
    for x, y, _, _, _, _ in hunters:
        predator_grid[y][x] = 1

    eaten_fish = set()  # Track which fish positions have been eaten
    new_hunters = []
    
    # HUNTERS MOVE FIRST
    for x, y, direction, age, starve_time, resource_level in hunters:
        # First, survey 8 neighbors for fish
        fish_pos = find_fish_neighbors_8(fish_grid, x, y, N)
        
        if fish_pos and fish_pos not in eaten_fish:
            # Found a fish that hasn't been eaten yet - move to it and eat it
            new_x, new_y = fish_pos
            fish_age = fish_dict[(new_x, new_y)]
            # Hunter gains resource equal to fish age, starve_time resets to 0
            new_hunters.append((new_x, new_y, direction, age + 1, 0, resource_level + fish_age))
            eaten_fish.add((new_x, new_y))
            predator_grid[new_y][new_x] = 1
            predator_grid[y][x] = 0
            fish_grid[new_y][new_x] = 0  # Remove the fish from the grid
        else:
            # No fish in 8 neighbors (or already eaten), move in direction like a shark
            new_x, new_y = get_direction_move(x, y, direction, N)
            
            # Check if target cell is free
            if predator_grid[new_y][new_x] == 0 and fish_grid[new_y][new_x] == 0:
                # Move to the new position
                new_hunters.append((new_x, new_y, direction, age + 1, starve_time + 1, resource_level - 1))
                predator_grid[new_y][new_x] = 1
                predator_grid[y][x] = 0
            else:
                # Can't move in direction, stay in place, resource still decreases
                new_hunters.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))

    # Update fish list after hunters have eaten
    remaining_fish = [(x, y, d, a) for x, y, d, a in fish if (x, y) not in eaten_fish]
    
    # Update fish_dict for sharks
    fish_dict = {(x, y): age for x, y, _, age in remaining_fish}
    
    new_sharks = []
    
    # SHARKS MOVE SECOND
    for x, y, direction, age, starve_time, resource_level in sharks:
        # Try to find fish in 4 neighbors
        fish_neighbors = find_fish_neighbors(fish_grid, x, y, N)
        # Filter out already eaten fish
        fish_neighbors = [pos for pos in fish_neighbors if pos not in eaten_fish]
        
        if fish_neighbors:
            # Eat a fish and move to its position
            new_x, new_y = fish_neighbors[np.random.randint(0, len(fish_neighbors))]
            fish_age = fish_dict[(new_x, new_y)]
            # Shark gains resource equal to fish age, starve_time resets to 0
            new_sharks.append((new_x, new_y, direction, age + 1, 0, resource_level + fish_age))
            eaten_fish.add((new_x, new_y))
            predator_grid[new_y][new_x] = 1
            predator_grid[y][x] = 0
            fish_grid[new_y][new_x] = 0  # Remove the fish from the grid
        else:
            # No fish nearby, move in direction
            new_x, new_y = get_direction_move(x, y, direction, N)
            
            # Check if target cell is free
            if predator_grid[new_y][new_x] == 0 and fish_grid[new_y][new_x] == 0:
                # Move to the new position
                new_sharks.append((new_x, new_y, direction, age + 1, starve_time + 1, resource_level - 1))
                predator_grid[new_y][new_x] = 1
                predator_grid[y][x] = 0
            else:
                # Can't move in direction, stay in place, resource still decreases
                new_sharks.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))

    # Remove all eaten fish from the fish list
    remaining_fish = [(x, y, d, a) for x, y, d, a in remaining_fish if (x, y) not in eaten_fish]

    # Remove starved sharks and hunters
    surviving_sharks = []
    for x, y, direction, age, starve_time, resource_level in new_sharks:
        if starve_time < shark_starving_time and resource_level >= 0:
            surviving_sharks.append((x, y, direction, age, starve_time, resource_level))

    surviving_hunters = []
    for x, y, direction, age, starve_time, resource_level in new_hunters:
        if starve_time < hunter_starving_time and resource_level >= 0:
            surviving_hunters.append((x, y, direction, age, starve_time, resource_level))

    # Update the predator grid after removing starved predators
    predator_grid = [[0 for _ in range(N)] for _ in range(N)]
    for x, y, _, _, _, _ in surviving_sharks:
        predator_grid[y][x] = 1
    for x, y, _, _, _, _ in surviving_hunters:
        predator_grid[y][x] = 1

    # Breed the sharks
    final_sharks = []
    shark_offspring = []
    for x, y, direction, age, starve_time, resource_level in surviving_sharks:
        if (age - 1) >= shark_breeding_time and resource_level > breeding_energy:
            breeding_neighbors = find_breeding_neighbors(predator_grid, x, y, N)
            if breeding_neighbors:
                new_x, new_y = breeding_neighbors[np.random.randint(0, len(breeding_neighbors))]
                parent_resource = resource_level // 2
                child_resource = resource_level - parent_resource
                final_sharks.append((x, y, direction, 0, starve_time, parent_resource))
                shark_offspring.append((new_x, new_y, direction, 0, 0, child_resource))
                predator_grid[new_y][new_x] = 1
            else:
                final_sharks.append((x, y, direction, age, starve_time, resource_level))
        else:
            final_sharks.append((x, y, direction, age, starve_time, resource_level))

    # Breed the hunters
    final_hunters = []
    hunter_offspring = []
    for x, y, direction, age, starve_time, resource_level in surviving_hunters:
        if (age - 1) >= hunter_breeding_time and resource_level > breeding_energy:
            breeding_neighbors = find_breeding_neighbors(predator_grid, x, y, N)
            if breeding_neighbors:
                new_x, new_y = breeding_neighbors[np.random.randint(0, len(breeding_neighbors))]
                parent_resource = resource_level // 2
                child_resource = resource_level - parent_resource
                final_hunters.append((x, y, direction, 0, starve_time, parent_resource))
                hunter_offspring.append((new_x, new_y, direction, 0, 0, child_resource))
                predator_grid[new_y][new_x] = 1
            else:
                final_hunters.append((x, y, direction, age, starve_time, resource_level))
        else:
            final_hunters.append((x, y, direction, age, starve_time, resource_level))

    return remaining_fish, final_sharks + shark_offspring, final_hunters + hunter_offspring

def simulate_step(N, fish, sharks, hunters, fish_breeding_time, shark_breeding_time, shark_starving_time, 
                  hunter_breeding_time, hunter_starving_time, breeding_energy):
    """
    Simulates one step of the Wa-Tor simulation, including fish, shark, and hunter behavior.
    """
    # Predators move first (combined to handle conflicts)
    fish, sharks, hunters = simulate_predator_step(N, fish, sharks, hunters, shark_breeding_time, 
                                                   shark_starving_time, hunter_breeding_time, 
                                                   hunter_starving_time, breeding_energy)
    # Then remaining fish move and breed
    fish = simulate_fish_step(N, fish, fish_breeding_time)
    
    return fish, sharks, hunters