#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Disease Dynamics Lattice Plot
#-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt

def lattice_plot(N, susceptible, infected):
    """
    Plots the grid with the susceptible and infected individuals.

    Args:
        N (int): Size of the grid.
        susceptible (list): List of susceptible agents.
        infected (list): List of infected agents.
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Disease Dynamics Simulation")
    ax.set_aspect('equal')

    img = np.full((N, N, 3), 255, dtype=np.uint8)  # White background

    for agent in susceptible:
        x, y = int(agent[0]), int(agent[1])
        if 0 <= x < N and 0 <= y < N:
            img[y, x] = [0, 255, 0]  # Green for susceptible

    for agent in infected:
        x, y = int(agent[0]), int(agent[1])
        if 0 <= x < N and 0 <= y < N:
            img[y, x] = [255, 0, 0]  # Red for infected

    ax.imshow(img, extent=[0, N, 0, N], interpolation='nearest')
    ax.set_xticks(np.arange(0, N + 1, 5))
    ax.set_yticks(np.arange(0, N + 1, 5))
    ax.grid(color='lightgray', linestyle='-', linewidth=0.5)

    plt.show()