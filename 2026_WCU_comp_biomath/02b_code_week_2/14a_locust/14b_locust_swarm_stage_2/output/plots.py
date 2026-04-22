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
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Separate airborne and grounded locusts
    airborne = ~grounded
    
    # Plot airborne locusts
    if np.any(airborne):
        ax.scatter(positions[airborne, 0], positions[airborne, 1], 
                  c='blue', s=80, alpha=0.7, label='Airborne', edgecolors='darkblue', linewidth=0.5)
    
    # Plot grounded locusts
    if np.any(grounded):
        ax.scatter(positions[grounded, 0], positions[grounded, 1], 
                  c='red', s=80, alpha=0.7, label='Grounded', edgecolors='darkred', linewidth=0.5)
    
    ax.set_xlabel('x (horizontal)', fontsize=14)
    ax.set_ylabel('z (vertical)', fontsize=14)
    ax.set_title(f'{title} (t = {time:.2f})', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Draw ground
    xlim = ax.get_xlim()
    ax.fill_between(xlim, -1, 0, color='brown', alpha=0.3, label='Ground')
    ax.axhline(y=0, color='brown', linestyle='-', linewidth=3)
    ax.set_xlim(xlim)
    
    # Set y limit to show ground
    ylim = ax.get_ylim()
    ax.set_ylim(min(ylim[0], -0.5), ylim[1])
    
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
    fig, ax = plt.subplots(figsize=(14, 7))
    
    N = history_positions[0].shape[0]
    if sample_indices is None:
        sample_indices = range(min(N, 10))  # Plot first 10 by default
    
    for i in sample_indices:
        traj_x = [pos[i, 0] for pos in history_positions]
        traj_z = [pos[i, 1] for pos in history_positions]
        ax.plot(traj_x, traj_z, alpha=0.6, linewidth=1.5)
        # Mark start and end
        ax.plot(traj_x[0], traj_z[0], 'go', markersize=8, alpha=0.7)
        ax.plot(traj_x[-1], traj_z[-1], 'rs', markersize=8, alpha=0.7)
    
    ax.set_xlabel('x (horizontal)', fontsize=14)
    ax.set_ylabel('z (vertical)', fontsize=14)
    ax.set_title('Locust Trajectories (green=start, red=end)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Draw ground
    xlim = ax.get_xlim()
    ax.fill_between(xlim, -1, 0, color='brown', alpha=0.3)
    ax.axhline(y=0, color='brown', linestyle='-', linewidth=3, label='Ground')
    ax.set_xlim(xlim)
    
    ylim = ax.get_ylim()
    ax.set_ylim(min(ylim[0], -0.5), ylim[1])
    ax.legend(fontsize=12)
    
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
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    
    # Mean height
    axes[0, 0].plot(times, diagnostics['mean_height'], 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Time', fontsize=12)
    axes[0, 0].set_ylabel('Mean Height', fontsize=12)
    axes[0, 0].set_title('Mean Height Over Time', fontsize=13, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0, color='brown', linestyle='--', linewidth=1)
    
    # Grounded count
    axes[0, 1].plot(times, diagnostics['grounded_count'], 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time', fontsize=12)
    axes[0, 1].set_ylabel('Grounded Count', fontsize=12)
    axes[0, 1].set_title('Number of Grounded Locusts', fontsize=13, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Swarm center x
    axes[0, 2].plot(times, diagnostics['center_x'], 'g-', linewidth=2)
    axes[0, 2].set_xlabel('Time', fontsize=12)
    axes[0, 2].set_ylabel('Center X', fontsize=12)
    axes[0, 2].set_title('Swarm Center (Horizontal)', fontsize=13, fontweight='bold')
    axes[0, 2].grid(True, alpha=0.3)
    
    # Swarm center z
    axes[1, 0].plot(times, diagnostics['center_z'], 'm-', linewidth=2)
    axes[1, 0].set_xlabel('Time', fontsize=12)
    axes[1, 0].set_ylabel('Center Z', fontsize=12)
    axes[1, 0].set_title('Swarm Center (Vertical)', fontsize=13, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=0, color='brown', linestyle='--', linewidth=1)
    
    # Width
    axes[1, 1].plot(times, diagnostics['width'], 'c-', linewidth=2)
    axes[1, 1].set_xlabel('Time', fontsize=12)
    axes[1, 1].set_ylabel('Width', fontsize=12)
    axes[1, 1].set_title('Swarm Width', fontsize=13, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Height
    axes[1, 2].plot(times, diagnostics['height'], 'y-', linewidth=2)
    axes[1, 2].set_xlabel('Time', fontsize=12)
    axes[1, 2].set_ylabel('Height', fontsize=12)
    axes[1, 2].set_title('Swarm Height', fontsize=13, fontweight='bold')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, axes

def plot_landing_analysis(times, diagnostics):
    """
    Plot analysis specific to landing behavior (Stage 2).
    
    Parameters:
    -----------
    times : ndarray
        Array of time points
    diagnostics : dict
        Dictionary of diagnostic time series
    
    Returns:
    --------
    fig, axes : matplotlib figure and axes
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Get grounded counts as numpy array
    grounded_counts = np.array(diagnostics['grounded_count'])
    
    # Infer N from maximum count (assumes at some point all might be grounded)
    # Or we can get it from the length of the first position array
    N_total = 50  # Default from parameters, or could be passed as argument
    
    # Calculate fraction grounded
    fraction_grounded = grounded_counts / N_total
    
    # Plot 1: Fraction grounded over time
    axes[0].plot(times, fraction_grounded, 'r-', linewidth=2.5)
    axes[0].fill_between(times, 0, fraction_grounded, alpha=0.3, color='red')
    axes[0].set_xlabel('Time', fontsize=13)
    axes[0].set_ylabel('Fraction Grounded', fontsize=13)
    axes[0].set_title('Landing Dynamics', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([0, 1.05])
    
    # Plot 2: Mean height vs grounded count (colored by time)
    scatter = axes[1].scatter(grounded_counts, diagnostics['mean_height'], 
                             c=times, cmap='viridis', s=30, alpha=0.7)
    axes[1].set_xlabel('Number Grounded', fontsize=13)
    axes[1].set_ylabel('Mean Height', fontsize=13)
    axes[1].set_title('Mean Height vs Grounded Count', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='brown', linestyle='--', linewidth=1, alpha=0.5)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=axes[1])
    cbar.set_label('Time', fontsize=11)
    
    plt.tight_layout()
    return fig, axes