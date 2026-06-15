#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (Lattice Plot)
#-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def lattice_plot(N, fish, sharks, hunters):
    """
    Plots the grid with the fish, sharks, and hunter sharks.
    Shows the sanctuary area as a green square.

    Args:
        N (int): Size of the grid.
        fish (list): List of fish agents.
        sharks (list): List of shark agents.
        hunters (list): List of hunter shark agents.
    """
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Wa-Tor Simulation with Sanctuary")
    ax.set_aspect('equal')

    # Create a new image for each frame
    img = np.full((N, N, 3), 255, dtype=np.uint8)  # White background

    # Draw the fish (blue)
    for agent in fish:
        x, y = int(agent[0]), int(agent[1])
        if 0 <= x < N and 0 <= y < N:
            img[y, x, 0] = 0  # Blue
            img[y, x, 1] = 0
            img[y, x, 2] = 255

    # Draw the sharks (red)
    for agent in sharks:
        x, y = int(agent[0]), int(agent[1])
        if 0 <= x < N and 0 <= y < N:
            img[y, x, 0] = 255  # Red
            img[y, x, 1] = 0
            img[y, x, 2] = 0

    # Draw the hunter sharks (orange)
    for agent in hunters:
        x, y = int(agent[0]), int(agent[1])
        if 0 <= x < N and 0 <= y < N:
            img[y, x, 0] = 255  # Orange
            img[y, x, 1] = 165
            img[y, x, 2] = 0

    # Plot the image with origin='upper' and flipped Y extent to match array indexing
    ax.imshow(img, extent=[0, N, N, 0], origin='upper', interpolation='nearest')
    
    # Draw the sanctuary - coordinates now match the agent positions
    sanctuary_start = N // 4
    sanctuary_size = N // 2
    sanctuary_rect = patches.Rectangle((sanctuary_start, sanctuary_start), 
                                      sanctuary_size, sanctuary_size,
                                      linewidth=3, edgecolor='green', 
                                      facecolor='none', label='Sanctuary')
    ax.add_patch(sanctuary_rect)
    
    ax.set_xticks(np.arange(0, N + 1, 5))
    ax.set_yticks(np.arange(0, N + 1, 5))
    ax.grid(color='lightgray', linestyle='-', linewidth=0.5)
    ax.legend(loc='upper right')

    plt.savefig('wa-tor_lattice.png')
    plt.close()
    print("Lattice plot saved as 'wa-tor_lattice.png'")