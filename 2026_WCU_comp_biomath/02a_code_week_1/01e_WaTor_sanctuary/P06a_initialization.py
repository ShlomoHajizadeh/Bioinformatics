#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

import numpy as np
from P06i_helpers import is_in_sanctuary

def initialize_predator_outside_sanctuary(N, occupied_positions):
    """
    Generate a random position outside the sanctuary that is not already occupied.
    Returns (x, y) coordinates.
    """
    max_attempts = 1000
    attempts = 0
    
    while attempts < max_attempts:
        x = np.random.randint(0, N)
        y = np.random.randint(0, N)
        
        if not is_in_sanctuary(x, y, N) and (x, y) not in occupied_positions:
            return x, y
        
        attempts += 1
    
    # If we can't find a spot after max_attempts, return None
    return None

def initialize_fish(N, num_fish):
    """
    Initialize fish population.
    Each fish: (x, y, direction, age)
    Fish can be placed anywhere including sanctuary.
    """
    fish = []
    occupied_positions = set()
    
    for _ in range(num_fish):
        # Find an unoccupied position
        while True:
            x = np.random.randint(0, N)
            y = np.random.randint(0, N)
            if (x, y) not in occupied_positions:
                occupied_positions.add((x, y))
                break
        
        direction = np.random.randint(1, 5)  # 1=North, 2=East, 3=South, 4=West
        age = 0
        fish.append((x, y, direction, age))
    
    return fish, occupied_positions

def initialize_sharks(N, num_sharks, occupied_positions):
    """
    Initialize shark population.
    Each shark: (x, y, direction, age, starve_time, resource_level)
    Sharks CANNOT be placed in sanctuary.
    Initial resource_level = 10 (default)
    """
    sharks = []
    initial_resource = 10
    
    for _ in range(num_sharks):
        pos = initialize_predator_outside_sanctuary(N, occupied_positions)
        
        if pos is None:
            print(f"Warning: Could only place {len(sharks)} sharks out of {num_sharks}")
            break
        
        x, y = pos
        occupied_positions.add((x, y))
        
        direction = np.random.randint(1, 5)  # 1=North, 2=East, 3=South, 4=West
        age = 0
        starve_time = 0
        resource_level = initial_resource
        
        sharks.append((x, y, direction, age, starve_time, resource_level))
    
    return sharks

def initialize_hunters(N, num_hunters, occupied_positions):
    """
    Initialize hunter population.
    Each hunter: (x, y, direction, age, starve_time, resource_level)
    Hunters CANNOT be placed in sanctuary.
    Initial resource_level = 15 (default)
    """
    hunters = []
    initial_resource = 15
    
    for _ in range(num_hunters):
        pos = initialize_predator_outside_sanctuary(N, occupied_positions)
        
        if pos is None:
            print(f"Warning: Could only place {len(hunters)} hunters out of {num_hunters}")
            break
        
        x, y = pos
        occupied_positions.add((x, y))
        
        direction = np.random.randint(1, 5)  # 1=North, 2=East, 3=South, 4=West
        age = 0
        starve_time = 0
        resource_level = initial_resource
        
        hunters.append((x, y, direction, age, starve_time, resource_level))
    
    return hunters

def initialize_agents(N, num_fish, num_sharks, num_hunters):
    """
    Initialize the complete Wa-Tor simulation.
    This function matches the signature expected by 06_WaTor.py
    
    Parameters:
    - N: Grid size (N x N)
    - num_fish: Number of fish to initialize
    - num_sharks: Number of sharks to initialize
    - num_hunters: Number of hunters to initialize
    
    Returns:
    - fish: List of fish tuples (x, y, direction, age)
    - sharks: List of shark tuples (x, y, direction, age, starve_time, resource_level)
    - hunters: List of hunter tuples (x, y, direction, age, starve_time, resource_level)
    """
    # Initialize fish first (they can go anywhere)
    fish, occupied_positions = initialize_fish(N, num_fish)
    
    # Initialize sharks (outside sanctuary only)
    sharks = initialize_sharks(N, num_sharks, occupied_positions)
    
    # Initialize hunters (outside sanctuary only)
    hunters = initialize_hunters(N, num_hunters, occupied_positions)
    
    print(f"Initialized simulation:")
    print(f"  Grid size: {N}x{N}")
    print(f"  Sanctuary: ({N//4}, {N//4}) to ({3*N//4}, {3*N//4})")
    print(f"  Fish: {len(fish)}")
    print(f"  Sharks: {len(sharks)}")
    print(f"  Hunters: {len(hunters)}")
    
    return fish, sharks, hunters