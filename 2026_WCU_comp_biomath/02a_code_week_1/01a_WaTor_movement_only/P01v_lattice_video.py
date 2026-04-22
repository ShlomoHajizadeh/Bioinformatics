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
import matplotlib.animation as animation
from P01m_movement import simulate_step

def lattice_animation(N, fish, sharks, num_steps):
    """
    Animates the Wa-Tor simulation on the lattice.

    Args:
        N (int): Size of the grid.
        fish (list): List of fish agents.
        sharks (list): List of shark agents.
        num_steps (int): Number of time steps to simulate.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title('Wa-Tor Simulation')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('white')

    def update_lattice(frame):
        nonlocal fish, sharks
        fish, sharks = simulate_step(N, fish, sharks)
        img = np.full((N, N, 3), 255, dtype=np.uint8)  # White background

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

        return [ax.imshow(img, extent=[0, N, 0, N], interpolation='nearest')]

    ani = animation.FuncAnimation(fig, update_lattice, frames=num_steps, interval=500, blit=True)

    # Save the animation as a GIF
    ani.save('wa-tor_simulation.gif', writer='pillow')

    plt.show(block=False)

    return ani

def time_plot(fish_history, shark_history):
    """
    Plots the time series of the fish and shark populations.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(fish_history, label='Fish', color='blue', linewidth=3)
    plt.plot(shark_history, label='Sharks', color='red', linewidth=3)
    plt.xlabel('Time step')
    plt.ylabel('Population')
    plt.title('Wa-Tor Simulation')
    plt.legend()
    plt.savefig('wa-tor_population_plot.png')
    plt.show()