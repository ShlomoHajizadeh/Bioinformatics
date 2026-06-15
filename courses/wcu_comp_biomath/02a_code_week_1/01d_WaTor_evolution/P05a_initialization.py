#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

import numpy as np

def initialize_agents(N, fish_count, shark_count, hunter_count):
    """
    Initializes the fish, shark, and hunter shark agents on a grid of size N x N.

    Args:
        N (int): Size of the grid.
        fish_count (int): Number of fish agents.
        shark_count (int): Number of shark agents.
        hunter_count (int): Number of hunter shark agents.

    Returns:
        fish (list): List of fish agents, each represented as a tuple (x, y, direction, age).
        sharks (list): List of shark agents, each represented as a tuple (x, y, direction, age, starve_time, resource_level).
        hunters (list): List of hunter shark agents, each represented as a tuple (x, y, direction, age, starve_time, resource_level).
    """
    # Create a 1D vector of indices
    indices = np.arange(N * N)

    # Shuffle the indices
    np.random.shuffle(indices)

    # Assign the first fish_count indices to fish
    fish_indices = indices[:fish_count]
    fish = [(i % N, i // N, np.random.randint(1, 5), 0) for i in fish_indices]

    # Assign the next shark_count indices to sharks
    # Sharks have 6 elements: (x, y, direction, age, starve_time, resource_level)
    shark_indices = indices[fish_count:fish_count + shark_count]
    sharks = [(i % N, i // N, np.random.randint(1, 5), 0, 0, 0) for i in shark_indices]

    # Assign the next hunter_count indices to hunter sharks
    # Hunters have 6 elements: (x, y, direction, age, starve_time, resource_level)
    hunter_indices = indices[fish_count + shark_count:fish_count + shark_count + hunter_count]
    hunters = [(i % N, i // N, np.random.randint(1, 5), 0, 0, 0) for i in hunter_indices]

    return fish, sharks, hunters