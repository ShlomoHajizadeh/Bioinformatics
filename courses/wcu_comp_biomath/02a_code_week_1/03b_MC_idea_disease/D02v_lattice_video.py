#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Disease Dynamics Lattice Animation
#-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from D02_interaction import simulate_step

def time_plot(susceptible_history, infected_history):
    """
    Plots the time series of the susceptible and infected populations.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(susceptible_history, label='Susceptible', color='green', linewidth=3)
    plt.plot(infected_history, label='Infected', color='red', linewidth=3)
    plt.xlabel('Time step')
    plt.ylabel('Population')
    plt.title('Disease Dynamics Simulation')
    plt.legend()
    plt.ylim(0, max(max(susceptible_history), max(infected_history)) + 10)
    plt.savefig('disease_population_plot.png')
    plt.show()

def lattice_animation(N, susceptible, infected, num_steps, infection_probability):
    """
    Animates the disease dynamics simulation on the lattice.

    Args:
        N (int): Size of the grid.
        susceptible (list): List of susceptible agents.
        infected (list): List of infected agents.
        num_steps (int): Number of time steps to simulate.
        infection_probability (float): Probability of a susceptible agent becoming infected.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title('Disease Dynamics Simulation')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('white')

    def update_lattice(frame):
        nonlocal susceptible, infected
        susceptible, infected = simulate_step(N, susceptible, infected, infection_probability)
        img = np.full((N, N, 3), 255, dtype=np.uint8)  # White background

        for agent in susceptible:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x] = [0, 255, 0]  # Green for susceptible

        for agent in infected:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x] = [255, 0, 0]  # Red for infected

        return [ax.imshow(img, extent=[0, N, 0, N], interpolation='nearest')]

    ani = animation.FuncAnimation(fig, update_lattice, frames=num_steps, interval=500, blit=True)

    # Save the animation as a GIF
    ani.save('disease_dynamics_simulation.gif', writer='pillow')

    plt.show(block=False)

    return ani