"""
Creates plots for visualization.
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_swarm_snapshot(positions, grounded, time, title="Swarm Snapshot"):
    """
    Create a scatter plot of the swarm at a given time.
    
    Parameters:
    -----------
    positions : ndarray
        Positions array of shape (N, 2)
    grounded : ndarray
        Boolean array of shape (N,)
    time : float
        Current simulation time
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Separate airborne and grounded locusts
    airborne = ~grounded
    
    # Plot airborne locusts
    if np.any(airborne):
        ax.scatter(positions[airborne, 0], positions[airborne, 1], 
                  c='blue', s=50, alpha=0.6, label='Airborne')
    
    # Plot grounded locusts
    if np.any(grounded):
        ax.scatter(positions[grounded, 0], positions[grounded, 1], 
                  c='red', s=50, alpha=0.6, label='Grounded')
    
    ax.set_xlabel('x (horizontal)', fontsize=12)
    ax.set_ylabel('z (vertical)', fontsize=12)
    ax.set_title(f'{title} (t = {time:.2f})', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='brown', linestyle='--', linewidth=2, label='Ground')
    ax.set_aspect('equal')
    
    return fig, ax

def plot_trajectories(history_positions, sample_indices=None):
    """
    Plot trajectories of selected locusts.
    
    Parameters:
    -----------
    history_positions : list
        List of position arrays
    sample_indices : list, optional
        Indices of locusts to plot (if None, plot all)
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    N = history_positions[0].shape[0]
    if sample_indices is None:
        sample_indices = range(min(N, 10))  # Plot first 10 by default
    
    for i in sample_indices:
        traj_x = [pos[i, 0] for pos in history_positions]
        traj_z = [pos[i, 1] for pos in history_positions]
        ax.plot(traj_x, traj_z, alpha=0.6, linewidth=1)
    
    ax.set_xlabel('x (horizontal)', fontsize=12)
    ax.set_ylabel('z (vertical)', fontsize=12)
    ax.set_title('Locust Trajectories', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='brown', linestyle='--', linewidth=2, label='Ground')
    
    return fig, ax

def plot_diagnostics(times, diagnostics):
    """
    Plot diagnostic time series.
    
    Parameters:
    -----------
    times : ndarray
        Array of time points
    diagnostics : dict
        Dictionary of diagnostic time series
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    # Mean height
    axes[0, 0].plot(times, diagnostics['mean_height'], 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('Mean Height')
    axes[0, 0].set_title('Mean Height Over Time')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Grounded count
    axes[0, 1].plot(times, diagnostics['grounded_count'], 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('Grounded Count')
    axes[0, 1].set_title('Number of Grounded Locusts')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Swarm center x
    axes[0, 2].plot(times, diagnostics['center_x'], 'g-', linewidth=2)
    axes[0, 2].set_xlabel('Time')
    axes[0, 2].set_ylabel('Center X')
    axes[0, 2].set_title('Swarm Center (Horizontal)')
    axes[0, 2].grid(True, alpha=0.3)
    
    # Swarm center z
    axes[1, 0].plot(times, diagnostics['center_z'], 'm-', linewidth=2)
    axes[1, 0].set_xlabel('Time')
    axes[1, 0].set_ylabel('Center Z')
    axes[1, 0].set_title('Swarm Center (Vertical)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Width
    axes[1, 1].plot(times, diagnostics['width'], 'c-', linewidth=2)
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Width')
    axes[1, 1].set_title('Swarm Width')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Height
    axes[1, 2].plot(times, diagnostics['height'], 'y-', linewidth=2)
    axes[1, 2].set_xlabel('Time')
    axes[1, 2].set_ylabel('Height')
    axes[1, 2].set_title('Swarm Height')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, axes