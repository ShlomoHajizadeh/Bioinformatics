#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Disease Dynamics Initialization
#-----------------------------------------

import numpy as np

def initialize_agents(N, susceptible_count, infected_count):
    """
    Initializes the susceptible and infected agents on a grid of size N x N.

    Args:
        N (int): Size of the grid.
        susceptible_count (int): Number of susceptible agents.
        infected_count (int): Number of infected agents.

    Returns:
        susceptible (list): List of susceptible agents, each represented as a tuple (x, y).
        infected (list): List of infected agents, each represented as a tuple (x, y).
    """
    indices = np.arange(N * N)
    np.random.shuffle(indices)

    susceptible_indices = indices[:susceptible_count]
    susceptible = [(i % N, i // N) for i in susceptible_indices]

    infected_indices = indices[susceptible_count:susceptible_count + infected_count]
    infected = [(i % N, i // N) for i in infected_indices]

    return susceptible, infected