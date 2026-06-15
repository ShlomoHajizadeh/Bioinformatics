"""
2D animation tools for boids simulations.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def animate_2d(history, config, filename='boids_2d.gif', fps=20):
    """
    Create 2D animation of boids simulation.
    
    Args:
        history: list of State objects
        config: Configuration object
        filename: output filename
        fps: frames per second
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Set up plot
    ax.set_xlim(0, config.domain_size[0])
    ax.set_ylim(0, config.domain_size[1])
    ax.set_aspect('equal')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Check if multi-species
    is_multispecies = hasattr(config, 'species1_label')
    
    if is_multispecies:
        # Initialize scatter plots for each species
        scatter1 = ax.scatter([], [], c='blue', s=20, alpha=0.6, label='Prey')
        scatter2 = ax.scatter([], [], c='red', s=100, alpha=0.8, marker='o', 
                            edgecolors='darkred', linewidths=1.5, label='Predators')
        ax.legend(loc='upper right', fontsize=12)
        ax.set_title('Predator-Prey System', fontsize=14)
    else:
        scatter = ax.scatter([], [], c='blue', s=20, alpha=0.6)
        ax.set_title('Boids Simulation', fontsize=14)
    
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                       verticalalignment='top', fontsize=12,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def init():
        """Initialize animation."""
        if is_multispecies:
            scatter1.set_offsets(np.empty((0, 2)))
            scatter2.set_offsets(np.empty((0, 2)))
            return scatter1, scatter2, time_text
        else:
            scatter.set_offsets(np.empty((0, 2)))
            return scatter, time_text
    
    def update(frame):
        """Update animation frame."""
        state = history[frame]
        time = frame * config.dt * config.save_every
        
        if is_multispecies:
            # Separate species
            mask1 = state.species == config.species1_label
            mask2 = state.species == config.species2_label
            
            # Update prey
            scatter1.set_offsets(state.positions[mask1])
            
            # Update predators
            scatter2.set_offsets(state.positions[mask2])
            
            time_text.set_text(f'Time: {time:.1f}\nPrey: {np.sum(mask1)}\nPredators: {np.sum(mask2)}')
            
            return scatter1, scatter2, time_text
        else:
            scatter.set_offsets(state.positions)
            time_text.set_text(f'Time: {time:.1f}')
            return scatter, time_text
    
    # Create animation
    n_frames = len(history)
    print(f"Creating animation with {n_frames} frames...")
    anim = FuncAnimation(fig, update, frames=n_frames, init_func=init,
                        blit=True, interval=1000/fps)
    
    # Save animation
    writer = PillowWriter(fps=fps)
    anim.save(filename, writer=writer)
    plt.close()
    
    print(f"Saved animation to {filename}")