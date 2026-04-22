#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (Animation)
#-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter

def lattice_animation(N, fish_history, shark_history, hunter_history, save_gif=False):
    """
    Creates an animation of the Wa-Tor simulation.
    
    Args:
        N (int): Size of the grid.
        fish_history (list): List of fish states for each time step.
        shark_history (list): List of shark states for each time step.
        hunter_history (list): List of hunter shark states for each time step.
        save_gif (bool): If True, saves animation as GIF instead of showing it.
    
    Returns:
        Animation object (or None if save_gif=True)
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal')
    
    # Draw the sanctuary rectangle (static)
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
    
    # Initialize the image with corrected extent and origin
    img = np.full((N, N, 3), 255, dtype=np.uint8)
    im = ax.imshow(img, extent=[0, N, N, 0], origin='upper', interpolation='nearest')
    
    title = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=12)
    
    def update(frame):
        """Update function for animation."""
        # Create new image
        img = np.full((N, N, 3), 255, dtype=np.uint8)
        
        # Draw fish (blue)
        for agent in fish_history[frame]:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x] = [0, 0, 255]
        
        # Draw sharks (red)
        for agent in shark_history[frame]:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x] = [255, 0, 0]
        
        # Draw hunter sharks (orange)
        for agent in hunter_history[frame]:
            x, y = int(agent[0]), int(agent[1])
            if 0 <= x < N and 0 <= y < N:
                img[y, x] = [255, 165, 0]
        
        im.set_array(img)
        title.set_text(f'Wa-Tor Simulation - Step {frame}\n'
                      f'Fish: {len(fish_history[frame])}, '
                      f'Sharks: {len(shark_history[frame])}, '
                      f'Hunters: {len(hunter_history[frame])}')
        return [im, title]
    
    num_frames = len(fish_history)
    ani = FuncAnimation(fig, update, frames=num_frames, interval=100, blit=True, repeat=True)
    
    if save_gif:
        print(f"Saving GIF with {num_frames} frames (this may take a while)...")
        writer = PillowWriter(fps=10)
        ani.save('wa-tor_animation.gif', writer=writer)
        plt.close()
        print("GIF saved!")
        return None
    else:
        plt.show()
        return ani


def time_plot(fish_counts, shark_counts, hunter_counts):
    """
    Plots the population dynamics over time.
    
    Args:
        fish_counts (list): Number of fish at each time step.
        shark_counts (list): Number of sharks at each time step.
        hunter_counts (list): Number of hunter sharks at each time step.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    time_steps = range(len(fish_counts))
    
    ax.plot(time_steps, fish_counts, label='Fish', color='blue', linewidth=2)
    ax.plot(time_steps, shark_counts, label='Sharks', color='red', linewidth=2)
    ax.plot(time_steps, hunter_counts, label='Hunter Sharks', color='orange', linewidth=2)
    
    ax.set_xlabel('Time Step', fontsize=12)
    ax.set_ylabel('Population', fontsize=12)
    ax.set_title('Wa-Tor Population Dynamics', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('wa-tor_population_plot.png')
    plt.close()
    print("Population plot saved as 'wa-tor_population_plot.png'")