"""
3D plotting for Reynolds boids simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_3d_snapshot(state, config, filename='boids_3d.png', show=False, elev=30, azim=45):
    """
    Create a snapshot plot of the 3D boids simulation.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
        show: whether to display the plot
        elev: elevation angle for viewing
        azim: azimuthal angle for viewing
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Get domain size
    Lx, Ly, Lz = config.domain_size
    
    # Get positions and velocities
    positions = state.positions
    velocities = state.velocities
    
    # Separate species
    mask_sp1 = state.get_species_mask(config.species1_label)
    mask_sp2 = state.get_species_mask(config.species2_label)
    
    # Plot species 1 (boids)
    if np.any(mask_sp1):
        pos_sp1 = positions[mask_sp1]
        vel_sp1 = velocities[mask_sp1]
        
        # Plot as arrows
        ax.quiver(pos_sp1[:, 0], pos_sp1[:, 1], pos_sp1[:, 2],
                 vel_sp1[:, 0], vel_sp1[:, 1], vel_sp1[:, 2],
                 color='blue', alpha=0.6, length=2, normalize=True,
                 arrow_length_ratio=0.3, label='Species 1 (Boids)')
    
    # Plot species 2 (avoidance only)
    if np.any(mask_sp2):
        pos_sp2 = positions[mask_sp2]
        vel_sp2 = velocities[mask_sp2]
        
        # Plot as arrows
        ax.quiver(pos_sp2[:, 0], pos_sp2[:, 1], pos_sp2[:, 2],
                 vel_sp2[:, 0], vel_sp2[:, 1], vel_sp2[:, 2],
                 color='red', alpha=0.8, length=2, normalize=True,
                 arrow_length_ratio=0.3, label='Species 2 (Avoidance)')
    
    # Set limits and labels
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_zlim(0, Lz)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('Reynolds Boids - 3D Snapshot', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    
    # Set viewing angle
    ax.view_init(elev=elev, azim=azim)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Add info text
    info_text = f"N = {state.n_agents} ({config.n_species1} + {config.n_species2})"
    ax.text2D(0.02, 0.98, info_text, transform=ax.transAxes,
              fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved plot to {filename}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_3d_projections(state, config, filename='boids_3d_projections.png'):
    """
    Plot 3D boids with 2D projections on each plane.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
    """
    fig = plt.figure(figsize=(15, 12))
    
    Lx, Ly, Lz = config.domain_size
    positions = state.positions
    
    mask_sp1 = state.get_species_mask(config.species1_label)
    mask_sp2 = state.get_species_mask(config.species2_label)
    
    # 3D plot
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    
    if np.any(mask_sp1):
        pos_sp1 = positions[mask_sp1]
        ax1.scatter(pos_sp1[:, 0], pos_sp1[:, 1], pos_sp1[:, 2],
                   c='blue', s=20, alpha=0.6, label='Species 1')
    
    if np.any(mask_sp2):
        pos_sp2 = positions[mask_sp2]
        ax1.scatter(pos_sp2[:, 0], pos_sp2[:, 1], pos_sp2[:, 2],
                   c='red', s=30, alpha=0.8, label='Species 2')
    
    ax1.set_xlim(0, Lx)
    ax1.set_ylim(0, Ly)
    ax1.set_zlim(0, Lz)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('3D View')
    ax1.legend()
    
    # XY projection
    ax2 = fig.add_subplot(2, 2, 2)
    if np.any(mask_sp1):
        ax2.scatter(positions[mask_sp1, 0], positions[mask_sp1, 1],
                   c='blue', s=20, alpha=0.6, label='Species 1')
    if np.any(mask_sp2):
        ax2.scatter(positions[mask_sp2, 0], positions[mask_sp2, 1],
                   c='red', s=30, alpha=0.8, label='Species 2')
    ax2.set_xlim(0, Lx)
    ax2.set_ylim(0, Ly)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('XY Projection')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # XZ projection
    ax3 = fig.add_subplot(2, 2, 3)
    if np.any(mask_sp1):
        ax3.scatter(positions[mask_sp1, 0], positions[mask_sp1, 2],
                   c='blue', s=20, alpha=0.6, label='Species 1')
    if np.any(mask_sp2):
        ax3.scatter(positions[mask_sp2, 0], positions[mask_sp2, 2],
                   c='red', s=30, alpha=0.8, label='Species 2')
    ax3.set_xlim(0, Lx)
    ax3.set_ylim(0, Lz)
    ax3.set_xlabel('X')
    ax3.set_ylabel('Z')
    ax3.set_title('XZ Projection')
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # YZ projection
    ax4 = fig.add_subplot(2, 2, 4)
    if np.any(mask_sp1):
        ax4.scatter(positions[mask_sp1, 1], positions[mask_sp1, 2],
                   c='blue', s=20, alpha=0.6, label='Species 1')
    if np.any(mask_sp2):
        ax4.scatter(positions[mask_sp2, 1], positions[mask_sp2, 2],
                   c='red', s=30, alpha=0.8, label='Species 2')
    ax4.set_xlim(0, Ly)
    ax4.set_ylim(0, Lz)
    ax4.set_xlabel('Y')
    ax4.set_ylabel('Z')
    ax4.set_title('YZ Projection')
    ax4.set_aspect('equal')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.suptitle('Reynolds Boids - 3D with Projections', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved projection plot to {filename}")
    plt.close()