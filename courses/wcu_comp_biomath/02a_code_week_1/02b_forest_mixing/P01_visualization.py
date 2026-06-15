"""
visualization.py

Functions for visualizing the forest model results.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation


def plot_lattice(lattice, title="Forest Lattice", filename=None, show=True):
    """
    Plot a single lattice state.
    
    Parameters
    ----------
    lattice : numpy.ndarray
        Lattice to plot (N x N array).
    title : str, optional
        Plot title.
    filename : str or None, optional
        If provided, save the figure to this filename.
    show : bool, optional
        If True, display the plot. Default is True.
    """
    # Define colors: Red for RO (0), Green for HI (1)
    colors = ['red', 'green']
    cmap = ListedColormap(colors)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(lattice, cmap=cmap, vmin=0, vmax=1, interpolation='nearest')
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    
    # Add colorbar with labels
    cbar = plt.colorbar(im, ax=ax, ticks=[0.25, 0.75])
    cbar.ax.set_yticklabels(['Red Oak (RO)', 'Hickory (HI)'])
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Saved lattice plot to {filename}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_time_series(counts_history, filename=None, show=True):
    """
    Plot the number of each species over time.
    
    Parameters
    ----------
    counts_history : numpy.ndarray
        Array of shape (T+1, 2) with counts of [RO, HI] at each time step.
    filename : str or None, optional
        If provided, save the figure to this filename.
    show : bool, optional
        If True, display the plot. Default is True.
    """
    T = counts_history.shape[0] - 1
    time_steps = np.arange(T + 1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot RO and HI counts
    ax.plot(time_steps, counts_history[:, 0], 'r-', linewidth=2, label='Red Oak (RO)')
    ax.plot(time_steps, counts_history[:, 1], 'g-', linewidth=2, label='Hickory (HI)')
    
    ax.set_xlabel('Time Step', fontsize=14)
    ax.set_ylabel('Number of Trees', fontsize=14)
    ax.set_title('Species Population Over Time', fontsize=16)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Saved time series plot to {filename}")
    
    if show:
        plt.show()
    else:
        plt.close()


def create_animation(history, filename='forest_animation.gif', interval=200):
    """
    Create an animation of the lattice evolution.
    
    Parameters
    ----------
    history : list of numpy.ndarray
        List of lattice states over time.
    filename : str, optional
        Filename to save the animation.
    interval : int, optional
        Delay between frames in milliseconds.
    """
    colors = ['red', 'green']
    cmap = ListedColormap(colors)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Initialize with first frame
    im = ax.imshow(history[0], cmap=cmap, vmin=0, vmax=1, interpolation='nearest')
    title = ax.set_title('Time Step: 0', fontsize=16)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    
    cbar = plt.colorbar(im, ax=ax, ticks=[0.25, 0.75])
    cbar.ax.set_yticklabels(['Red Oak (RO)', 'Hickory (HI)'])
    
    def update(frame):
        """Update function for animation."""
        im.set_array(history[frame])
        title.set_text(f'Time Step: {frame}')
        return [im, title]
    
    anim = FuncAnimation(fig, update, frames=len(history), 
                         interval=interval, blit=True, repeat=True)
    
    # Save animation
    anim.save(filename, writer='pillow', fps=1000//interval)
    print(f"Saved animation to {filename}")
    
    plt.close()


def print_statistics(counts_history):
    """
    Print statistics about the simulation.
    
    Parameters
    ----------
    counts_history : numpy.ndarray
        Array of shape (T+1, 2) with counts of [RO, HI] at each time step.
    """
    total_cells = counts_history[0].sum()
    
    # Initial statistics
    initial_RO = counts_history[0, 0]
    initial_HI = counts_history[0, 1]
    initial_RO_pct = 100 * initial_RO / total_cells
    initial_HI_pct = 100 * initial_HI / total_cells
    
    # Final statistics
    final_RO = counts_history[-1, 0]
    final_HI = counts_history[-1, 1]
    final_RO_pct = 100 * final_RO / total_cells
    final_HI_pct = 100 * final_HI / total_cells
    
    print("\n" + "="*60)
    print("SIMULATION STATISTICS")
    print("="*60)
    print(f"Total cells: {total_cells}")
    print(f"\nInitial state:")
    print(f"  Red Oak (RO):  {initial_RO:5d} trees ({initial_RO_pct:5.2f}%)")
    print(f"  Hickory (HI):  {initial_HI:5d} trees ({initial_HI_pct:5.2f}%)")
    print(f"\nFinal state:")
    print(f"  Red Oak (RO):  {final_RO:5d} trees ({final_RO_pct:5.2f}%)")
    print(f"  Hickory (HI):  {final_HI:5d} trees ({final_HI_pct:5.2f}%)")
    print(f"\nChange:")
    print(f"  Red Oak (RO):  {final_RO - initial_RO:+6d} trees ({final_RO_pct - initial_RO_pct:+6.2f}%)")
    print(f"  Hickory (HI):  {final_HI - initial_HI:+6d} trees ({final_HI_pct - initial_HI_pct:+6.2f}%)")
    print("="*60 + "\n")