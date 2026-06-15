#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Disease Dynamics Movement
#-----------------------------------------

import numpy as np

def simulate_step(N, susceptible, infected, infection_probability):
    """
    Simulates one step of the disease dynamics simulation with interactions.

    Args:
        N (int): Size of the grid.
        susceptible (list): List of susceptible agents.
        infected (list): List of infected agents.
        infection_probability (float): Probability of a susceptible agent becoming infected.

    Returns:
        susceptible (list): Updated list of susceptible agents.
        infected (list): Updated list of infected agents.
    """
    new_susceptible = []
    new_infected = []

    # Create a set of occupied positions for quick lookup
    occupied_positions = {(x, y) for x, y in susceptible} | {(x, y) for x, y in infected}

    # Move susceptible individuals
    for x, y in susceptible:
        dx, dy = np.random.randint(-1, 2), np.random.randint(-1, 2)  # Random movement
        new_x = (x + dx) % N
        new_y = (y + dy) % N

        # Check if the new cell is occupied
        if (new_x, new_y) in occupied_positions:
            # Interaction occurs
            for inf_x, inf_y in infected:
                if (new_x, new_y) == (inf_x, inf_y):
                    # Probability of becoming infected
                    if np.random.rand() < infection_probability:
                        new_infected.append((new_x, new_y))  # Become infected
                    else:
                        new_susceptible.append((x, y))  # Stay susceptible
                    break
            else:
                new_susceptible.append((x, y))  # No action if not infected
        else:
            new_susceptible.append((new_x, new_y))  # Move to new position

    # Move infected individuals
    for x, y in infected:
        dx, dy = np.random.randint(-1, 2), np.random.randint(-1, 2)  # Random movement
        new_x = (x + dx) % N
        new_y = (y + dy) % N

        # Check if the new cell is occupied
        if (new_x, new_y) in occupied_positions:
            # Interaction occurs, but infected agents do not change state
            new_infected.append((x, y))  # Stay in place
        else:
            new_infected.append((new_x, new_y))  # Move to new position

    return new_susceptible, new_infected