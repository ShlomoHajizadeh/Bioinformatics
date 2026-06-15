"""
3D plotting functions for boids simulations.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_3d_snapshot(state, config, filename='boids_3d_snapshot.png'):
    """
    Plot current state of 3D simulation.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Check if multi-species
    if hasattr(config, 'species1_label'):
        mask1 = state.species == config.species1_label
        mask2 = state.species == config.species2_label
        
        # Plot prey (blue dots)
        ax.scatter(state.positions[mask1, 0], state.positions[mask1, 1], state.positions[mask1, 2],
                  c='blue', s=20, alpha=0.6, label='Prey')
        
        # Plot predators (red dots)
        ax.scatter(state.positions[mask2, 0], state.positions[mask2, 1], state.positions[mask2, 2],
                  c='red', s=100, alpha=0.8, edgecolors='darkred',
                  linewidths=1.5, label='Predators')
        
        ax.legend(loc='upper right', fontsize=12)
        ax.set_title(f'3D Predator-Prey System (Prey: {np.sum(mask1)}, Predators: {np.sum(mask2)})',
                    fontsize=14)
    else:
        # Single species - blue dots
        ax.scatter(state.positions[:, 0], state.positions[:, 1], state.positions[:, 2],
                  c='blue', s=20, alpha=0.6)
        ax.set_title(f'3D Boids Simulation ({state.n_agents} agents)', fontsize=14)
    
    ax.set_xlim(0, config.domain_size[0])
    ax.set_ylim(0, config.domain_size[1])
    ax.set_zlim(0, config.domain_size[2])
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved plot to {filename}")


def plot_3d_final(state, config, filename='boids_3d_final.png'):
    """
    Plot final state of 3D simulation.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
    """
    plot_3d_snapshot(state, config, filename)


def plot_3d_projections(state, config, filename='boids_3d_projections.png'):
    """
    Plot 3D state with 2D projections on XY, XZ, and YZ planes.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
    """
    fig = plt.figure(figsize=(15, 12))
    
    # Check if multi-species
    is_multispecies = hasattr(config, 'species1_label')
    
    if is_multispecies:
        mask1 = state.species == config.species1_label
        mask2 = state.species == config.species2_label
    
    # 3D plot
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    if is_multispecies:
        ax1.scatter(state.positions[mask1, 0], state.positions[mask1, 1], state.positions[mask1, 2],
                   c='blue', s=20, alpha=0.6, label='Prey')
        ax1.scatter(state.positions[mask2, 0], state.positions[mask2, 1], state.positions[mask2, 2],
                   c='red', s=100, alpha=0.8, edgecolors='darkred', linewidths=1.5, label='Predators')
        ax1.legend()
    else:
        ax1.scatter(state.positions[:, 0], state.positions[:, 1], state.positions[:, 2],
                   c='blue', s=20, alpha=0.6)
    
    ax1.set_xlim(0, config.domain_size[0])
    ax1.set_ylim(0, config.domain_size[1])
    ax1.set_zlim(0, config.domain_size[2])
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('3D View')
    
    # XY projection
    ax2 = fig.add_subplot(2, 2, 2)
    if is_multispecies:
        ax2.scatter(state.positions[mask1, 0], state.positions[mask1, 1],
                   c='blue', s=20, alpha=0.6, label='Prey')
        ax2.scatter(state.positions[mask2, 0], state.positions[mask2, 1],
                   c='red', s=100, alpha=0.8, edgecolors='darkred', linewidths=1.5, label='Predators')
    else:
        ax2.scatter(state.positions[:, 0], state.positions[:, 1],
                   c='blue', s=20, alpha=0.6)
    
    ax2.set_xlim(0, config.domain_size[0])
    ax2.set_ylim(0, config.domain_size[1])
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('XY Projection (Top View)')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # XZ projection
    ax3 = fig.add_subplot(2, 2, 3)
    if is_multispecies:
        ax3.scatter(state.positions[mask1, 0], state.positions[mask1, 2],
                   c='blue', s=20, alpha=0.6, label='Prey')
        ax3.scatter(state.positions[mask2, 0], state.positions[mask2, 2],
                   c='red', s=100, alpha=0.8, edgecolors='darkred', linewidths=1.5, label='Predators')
    else:
        ax3.scatter(state.positions[:, 0], state.positions[:, 2],
                   c='blue', s=20, alpha=0.6)
    
    ax3.set_xlim(0, config.domain_size[0])
    ax3.set_ylim(0, config.domain_size[2])
    ax3.set_xlabel('X')
    ax3.set_ylabel('Z')
    ax3.set_title('XZ Projection (Front View)')
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    
    # YZ projection
    ax4 = fig.add_subplot(2, 2, 4)
    if is_multispecies:
        ax4.scatter(state.positions[mask1, 1], state.positions[mask1, 2],
                   c='blue', s=20, alpha=0.6, label='Prey')
        ax4.scatter(state.positions[mask2, 1], state.positions[mask2, 2],
                   c='red', s=100, alpha=0.8, edgecolors='darkred', linewidths=1.5, label='Predators')
    else:
        ax4.scatter(state.positions[:, 1], state.positions[:, 2],
                   c='blue', s=20, alpha=0.6)
    
    ax4.set_xlim(0, config.domain_size[1])
    ax4.set_ylim(0, config.domain_size[2])
    ax4.set_xlabel('Y')
    ax4.set_ylabel('Z')
    ax4.set_title('YZ Projection (Side View)')
    ax4.set_aspect('equal')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved projections to {filename}")