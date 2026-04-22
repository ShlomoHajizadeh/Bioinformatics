#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (1st Implementation)
#-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt

def lattice_plot(N, fish, sharks):
    """
    Plots the grid with the fish and sharks.

    Args:
        N (int): Size of the grid.
        fish (list): List of fish agents.
        sharks (list): List of shark agents.
    """
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Wa-Tor Simulation")
    ax.set_aspect('equal')

    # Create a new image for each frame
    img = np.full((N, N, 3), 255, dtype=np.uint8)  # White background

    # Draw the fish and sharks on the image
    for agent in fish:
        x, y = int(agent[0]), int(agent[1])
        if 0 <= x < N and 0 <= y < N:
            img[y, x, 0] = 0  # Blue
            img[y, x, 1] = 0
            img[y, x, 2] = 255

    for agent in sharks:
        x, y = int(agent[0]), int(agent[1])
        if 0 <= x < N and 0 <= y < N:
            img[y, x, 0] = 255  # Red
            img[y, x, 1] = 0
            img[y, x, 2] = 0

    # Plot the image
    ax.imshow(img, extent=[0, N, 0, N], interpolation='nearest')
    ax.set_xticks(np.arange(0, N + 1, 5))
    ax.set_yticks(np.arange(0, N + 1, 5))
    ax.grid(color='lightgray', linestyle='-', linewidth=0.5)

    # Save instead of showing
    plt.savefig('wa-tor_lattice.png')
    plt.close()  # Close the figure to free memory
    print("Lattice plot saved as 'wa-tor_lattice.png'")