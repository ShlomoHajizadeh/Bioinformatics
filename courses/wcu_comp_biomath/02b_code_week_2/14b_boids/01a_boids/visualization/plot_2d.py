"""
2D plotting for Reynolds boids simulation.
"""
import numpy as np
import matplotlib.pyplot as plt


def plot_2d_snapshot(state, config, filename='boids_2d.png', show=False):
    """
    Create a snapshot plot of the 2D boids simulation.
    
    Args:
        state: State object
        config: Configuration object
        filename: output filename
        show: whether to display the plot
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Get domain size
    Lx, Ly = config.domain_size
    
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
        ax.quiver(pos_sp1[:, 0], pos_sp1[:, 1],
                 vel_sp1[:, 0], vel_sp1[:, 1],
                 color='blue', alpha=0.6, scale=20, width=0.003,
                 label='Species 1 (Boids)')
    
    # Plot species 2 (avoidance only)
    if np.any(mask_sp2):
        pos_sp2 = positions[mask_sp2]
        vel_sp2 = velocities[mask_sp2]
        
        # Plot as arrows
        ax.quiver(pos_sp2[:, 0], pos_sp2[:, 1],
                 vel_sp2[:, 0], vel_sp2[:, 1],
                 color='red', alpha=0.8, scale=20, width=0.004,
                 label='Species 2 (Avoidance)')
    
    # Set limits and labels
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_aspect('equal')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('Reynolds Boids - 2D Snapshot', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Add info text
    info_text = f"N = {state.n_agents} ({config.n_species1} + {config.n_species2})"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved plot to {filename}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_2d_with_neighbors(state, config, agent_idx, filename='boids_2d_neighbors.png'):
    """
    Plot showing neighbors of a specific agent.
    
    Args:
        state: State object
        config: Configuration object
        agent_idx: index of agent to highlight
        filename: output filename
    """
    from core.domain import Domain
    from core.neighbors import find_neighbors_efficient
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    domain = Domain(config.domain_size)
    Lx, Ly = config.domain_size
    
    positions = state.positions
    velocities = state.velocities
    
    # Get parameters for the agent
    species_label = state.species[agent_idx]
    params = config.get_species_params(species_label)
    
    # Find neighbors
    neighbors_avoid = find_neighbors_efficient(state, domain, params['r_avoidance'])
    
    # Plot all agents
    mask_sp1 = state.get_species_mask(config.species1_label)
    mask_sp2 = state.get_species_mask(config.species2_label)
    
    # Plot species 1
    if np.any(mask_sp1):
        pos_sp1 = positions[mask_sp1]
        ax.scatter(pos_sp1[:, 0], pos_sp1[:, 1], c='blue', s=20, alpha=0.3, label='Species 1')
    
    # Plot species 2
    if np.any(mask_sp2):
        pos_sp2 = positions[mask_sp2]
        ax.scatter(pos_sp2[:, 0], pos_sp2[:, 1], c='red', s=20, alpha=0.3, label='Species 2')
    
    # Highlight focal agent
    ax.scatter(positions[agent_idx, 0], positions[agent_idx, 1],
              c='green', s=200, marker='*', edgecolors='black', linewidths=2,
              label='Focal agent', zorder=10)
    
    # Draw interaction radii
    circle_avoid = plt.Circle(positions[agent_idx], params['r_avoidance'],
                             color='orange', fill=False, linestyle='--',
                             linewidth=2, label='Avoidance radius')
    ax.add_patch(circle_avoid)
    
    if params['full_rules']:
        circle_align = plt.Circle(positions[agent_idx], params['r_alignment'],
                                 color='cyan', fill=False, linestyle=':',
                                 linewidth=2, label='Alignment radius')
        ax.add_patch(circle_align)
    
    # Highlight neighbors
    if neighbors_avoid[agent_idx]:
        neighbor_pos = positions[neighbors_avoid[agent_idx]]
        ax.scatter(neighbor_pos[:, 0], neighbor_pos[:, 1],
                  c='orange', s=100, marker='o', edgecolors='black',
                  linewidths=1, label='Neighbors', zorder=5)
    
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_aspect('equal')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title(f'Agent {agent_idx} and its Neighbors', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved neighbor plot to {filename}")
    plt.close()