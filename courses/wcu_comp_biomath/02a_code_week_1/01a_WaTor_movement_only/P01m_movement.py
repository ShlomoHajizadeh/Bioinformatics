#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (1st Implementation)
#-----------------------------------------

import numpy as np

def simulate_step(N, fish, sharks):
    """
    Simulates one step of the Wa-Tor simulation.

    Args:
        N (int): Size of the grid.
        fish (list): List of fish agents.
        sharks (list): List of shark agents.

    Returns:
        fish (list): Updated list of fish agents.
        sharks (list): Updated list of shark agents.
    """
    # Simulate fish movement
    new_fish = []
    for x, y, direction in fish:
        dx, dy = 0, 0
        if direction == 1:
            dy = 1
        elif direction == 2:
            dx = 1
        elif direction == 3:
            dy = -1
        elif direction == 4:
            dx = -1

        new_x = (x + dx) % N
        new_y = (y + dy) % N

        # Check if the new cell is unoccupied
        if (new_x, new_y) not in fish and (new_x, new_y) not in sharks:
            new_fish.append((new_x, new_y, direction))
        else:
            # If the new cell is occupied, try to move in the same direction
            new_x = x
            new_y = y
            for _ in range(N):
                new_x = (new_x + dx) % N
                new_y = (new_y + dy) % N
                if (new_x, new_y) not in fish and (new_x, new_y) not in sharks:
                    new_fish.append((new_x, new_y, direction))
                    break
            else:
                # If no unoccupied cell in the current direction, choose a new random direction
                new_direction = np.random.randint(1, 5)
                new_fish.append((x, y, new_direction))
    fish = new_fish

    # Simulate shark movement
    new_sharks = []
    for x, y, direction in sharks:
        dx, dy = 0, 0
        if direction == 1:
            dy = 1
        elif direction == 2:
            dx = 1
        elif direction == 3:
            dy = -1
        elif direction == 4:
            dx = -1

        new_x = (x + dx) % N
        new_y = (y + dy) % N

        # Check if the new cell is unoccupied
        if (new_x, new_y) not in fish and (new_x, new_y) not in sharks:
            new_sharks.append((new_x, new_y, direction))
        else:
            # If the new cell is occupied, try to move in the same direction
            new_x = x
            new_y = y
            for _ in range(N):
                new_x = (new_x + dx) % N
                new_y = (new_y + dy) % N
                if (new_x, new_y) not in fish and (new_x, new_y) not in sharks:
                    new_sharks.append((new_x, new_y, direction))
                    break
            else:
                # If no unoccupied cell in the current direction, choose a new random direction
                new_direction = np.random.randint(1, 5)
                new_sharks.append((x, y, new_direction))
    sharks = new_sharks

    return fish, sharks