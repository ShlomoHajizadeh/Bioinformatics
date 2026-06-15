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
    Find neighboring cells that contain fish.
    """
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if fish_grid[new_y][new_x] == 1:
            neighbors.append((new_x, new_y))
    return neighbors

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

def simulate_shark_step(N, fish, sharks, shark_breeding_time, shark_starving_time, breeding_energy):
    """
    Simulates one step of the shark simulation, including movement, eating, breeding, and starvation.
    
    Args:
        breeding_energy (int): Minimum resource level required for a shark to breed.
    """
    # Create grids to track fish and shark positions
    # Also create a dictionary to quickly look up fish by position
    fish_grid = [[0 for _ in range(N)] for _ in range(N)]
    shark_grid = [[0 for _ in range(N)] for _ in range(N)]
    fish_dict = {}  # Maps (x, y) to fish age
    
    for x, y, _, age in fish:
        fish_grid[y][x] = 1
        fish_dict[(x, y)] = age
    
    for x, y, _, _, _, _ in sharks:
        shark_grid[y][x] = 1

    new_sharks = []
    eaten_fish = set()  # Track which fish positions have been eaten
    
    for x, y, direction, age, starve_time, resource_level in sharks:
        # First, try to find fish to eat
        fish_neighbors = find_fish_neighbors(fish_grid, x, y, N)
        
        if fish_neighbors:
            # Eat a fish and move to its position
            new_x, new_y = fish_neighbors[np.random.randint(0, len(fish_neighbors))]
            fish_age = fish_dict[(new_x, new_y)]
            # Shark gains resource equal to fish age, starve_time resets to 0
            new_sharks.append((new_x, new_y, direction, age + 1, 0, resource_level + fish_age))
            eaten_fish.add((new_x, new_y))
            shark_grid[new_y][new_x] = 1
            shark_grid[y][x] = 0
            fish_grid[new_y][new_x] = 0  # Remove the fish from the grid
        else:
            # No fish nearby, try to move to an empty cell
            # Resource level decreases by 1
            movement_neighbors = find_movement_neighbors(shark_grid, x, y, N)
            if movement_neighbors:
                new_x, new_y = movement_neighbors[np.random.randint(0, len(movement_neighbors))]
                new_sharks.append((new_x, new_y, direction, age + 1, starve_time + 1, resource_level - 1))
                shark_grid[new_y][new_x] = 1
                shark_grid[y][x] = 0
            else:
                # Can't move, stay in place, resource still decreases
                new_sharks.append((x, y, direction, age + 1, starve_time + 1, resource_level - 1))

    # Remove eaten fish from the fish list
    remaining_fish = [(x, y, d, a) for x, y, d, a in fish if (x, y) not in eaten_fish]

    # Remove starved sharks (starve_time >= shark_starving_time OR resource_level < 0)
    surviving_sharks = []
    for x, y, direction, age, starve_time, resource_level in new_sharks:
        if starve_time < shark_starving_time and resource_level >= 0:
            surviving_sharks.append((x, y, direction, age, starve_time, resource_level))

    # Update the grid after removing starved sharks
    shark_grid = [[0 for _ in range(N)] for _ in range(N)]
    for x, y, _, _, _, _ in surviving_sharks:
        shark_grid[y][x] = 1

    # Breed the sharks
    final_sharks = []
    offspring = []
    for x, y, direction, age, starve_time, resource_level in surviving_sharks:
        # Shark can breed if: age >= shark_breeding_time AND resource_level > breeding_energy
        if (age - 1) >= shark_breeding_time and resource_level > breeding_energy:
            breeding_neighbors = find_breeding_neighbors(shark_grid, x, y, N)
            if breeding_neighbors:
                new_x, new_y = breeding_neighbors[np.random.randint(0, len(breeding_neighbors))]
                # Split resource level between parent and child
                parent_resource = resource_level // 2
                child_resource = resource_level - parent_resource
                final_sharks.append((x, y, direction, 0, starve_time, parent_resource))  # Parent with age reset to 0
                offspring.append((new_x, new_y, direction, 0, 0, child_resource))  # Offspring with age 0, starve_time 0
                shark_grid[new_y][new_x] = 1
            else:
                final_sharks.append((x, y, direction, age, starve_time, resource_level))  # Parent keeps its age if can't breed
        else:
            final_sharks.append((x, y, direction, age, starve_time, resource_level))  # Shark not ready to breed

    return remaining_fish, final_sharks + offspring

def simulate_step(N, fish, sharks, fish_breeding_time, shark_breeding_time, shark_starving_time, breeding_energy):
    """
    Simulates one step of the Wa-Tor simulation, including fish and shark behavior.
    """
    # IMPORTANT: Sharks move first and eat fish
    fish, sharks = simulate_shark_step(N, fish, sharks, shark_breeding_time, shark_starving_time, breeding_energy)
    # Then remaining fish move and breed
    fish = simulate_fish_step(N, fish, fish_breeding_time)
    return fish, sharks