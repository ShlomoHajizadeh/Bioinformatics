"""
2D plotting functions for boids simulations.
"""
import numpy as np
import matplotlib.pyplot as plt


def plot_2d_snapshot(state, config, filename='boids_2d_snapshot.png'):
    """
    Plot current state of 2D simulation.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Check if multi-species
    if hasattr(config, 'species1_label'):
        # Separate species
        mask1 = state.species == config.species1_label
        mask2 = state.species == config.species2_label
        
        # Plot prey (blue dots)
        ax.scatter(state.positions[mask1, 0], state.positions[mask1, 1],
                  c='blue', s=20, alpha=0.6, label='Prey')
        
        # Plot predators (red dots)
        ax.scatter(state.positions[mask2, 0], state.positions[mask2, 1],
                  c='red', s=100, alpha=0.8, edgecolors='darkred', 
                  linewidths=1.5, label='Predators')
        
        ax.legend(loc='upper right', fontsize=12)
        ax.set_title(f'Predator-Prey System (Prey: {np.sum(mask1)}, Predators: {np.sum(mask2)})', 
                    fontsize=14)
    else:
        # Single species - blue dots
        ax.scatter(state.positions[:, 0], state.positions[:, 1],
                  c='blue', s=20, alpha=0.6)
        ax.set_title(f'Boids Simulation ({state.n_agents} agents)', fontsize=14)
    
    ax.set_xlim(0, config.domain_size[0])
    ax.set_ylim(0, config.domain_size[1])
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved plot to {filename}")


def plot_2d_final(state, config, filename='boids_2d_final.png'):
    """
    Plot final state of 2D simulation.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
    """
    plot_2d_snapshot(state, config, filename)