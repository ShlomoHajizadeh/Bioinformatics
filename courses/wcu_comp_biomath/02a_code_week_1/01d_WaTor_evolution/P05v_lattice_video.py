#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def lattice_animation(N, fish_states, shark_states, hunter_states, save_gif=True):
    """
    Animates the Wa-Tor simulation on the lattice using pre-computed states.

    Args:
        N (int): Size of the grid.
        fish_states (list): List of fish states at each time step.
        shark_states (list): List of shark states at each time step.
        hunter_states (list): List of hunter shark states at each time step.
        save_gif (bool): Whether to save the animation as a GIF.
    """
    num_steps = len(fish_states)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title('Wa-Tor Simulation - Step 0')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('white')

    def update_lattice(frame):
        ax.clear()
        ax.set_title(f'Wa-Tor Simulation - Step {frame}')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor('white')
        
        fish = fish_states[frame]
        sharks = shark_states[frame]
        hunters = hunter_states[frame]
        
        img = np.full((N, N, 3), 255, dtype=np.uint8)  # White background

        # Draw fish (blue) - fish have 4 elements: (x, y, direction, age)
        for agent in fish:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x, 0] = 0  # Blue
                img[y, x, 1] = 0
                img[y, x, 2] = 255

        # Draw sharks (red) - sharks have 6 elements: (x, y, direction, age, starve_time, resource_level)
        for agent in sharks:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x, 0] = 255  # Red
                img[y, x, 1] = 0
                img[y, x, 2] = 0

        # Draw hunter sharks (orange) - hunters have 6 elements: (x, y, direction, age, starve_time, resource_level)
        for agent in hunters:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x, 0] = 255  # Orange
                img[y, x, 1] = 165
                img[y, x, 2] = 0

        ax.imshow(img, extent=[0, N, 0, N], interpolation='nearest')
        return [ax]

    ani = animation.FuncAnimation(fig, update_lattice, frames=num_steps, interval=200, blit=False, repeat=True)

    if save_gif:
        print(f"Saving GIF with {num_steps} frames (this may take a while)...")
        ani.save('wa-tor_simulation.gif', writer='pillow', fps=5)
        print("GIF saved!")
        plt.close()
    else:
        plt.show(block=False)

    return ani

def time_plot(fish_history, shark_history, hunter_history):
    """
    Plots the time series of the fish, shark, and hunter shark populations.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(fish_history, label='Fish', color='blue', linewidth=3)
    plt.plot(shark_history, label='Sharks', color='red', linewidth=3)
    plt.plot(hunter_history, label='Hunter Sharks', color='orange', linewidth=3)
    plt.xlabel('Time step')
    plt.ylabel('Population')
    plt.title('Wa-Tor Simulation')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('wa-tor_population_plot.png')
    plt.close()  # Close the figure
    print("Population plot saved as 'wa-tor_population_plot.png'")