#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Disease Dynamics Simulation
#-----------------------------------------

import numpy as np

def simulate_step(N, susceptible, infected):
    """
    Simulates one step of the disease dynamics simulation without changing populations.

    Args:
        N (int): Size of the grid.
        susceptible (list): List of susceptible agents.
        infected (list): List of infected agents.

    Returns:
        susceptible (list): Updated list of susceptible agents (remains constant).
        infected (list): Updated list of infected agents (remains constant).
    """
    # New lists to store the positions
    new_susceptible = []
    new_infected = []

    # Move susceptible individuals
    for x, y in susceptible:
        dx, dy = np.random.randint(-1, 2), np.random.randint(-1, 2)  # Random movement
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        new_susceptible.append((new_x, new_y))  # Keep moving but not changing the population

    # Move infected individuals
    for x, y in infected:
        dx, dy = np.random.randint(-1, 2), np.random.randint(-1, 2)  # Random movement
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        new_infected.append((new_x, new_y))  # Keep moving but not changing the population

    return new_susceptible, new_infected