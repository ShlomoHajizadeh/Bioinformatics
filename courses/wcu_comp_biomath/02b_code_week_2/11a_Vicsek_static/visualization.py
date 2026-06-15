"""Visualization functions for Vicsek model."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from config import VicsekConfig
from diagnostics import compute_velocities


def plot_state(positions: np.ndarray, headings: np.ndarray, 
               config: VicsekConfig, ax=None, arrow_scale=0.3):
    """Plot current state of the Vicsek model.
    
    Args:
        positions: Array of shape (N, 2) with particle positions
        headings: Array of shape (N,) with particle headings
        config: Vicsek configuration parameters
        ax: Matplotlib axis (creates new if None)
        arrow_scale: Scale factor for velocity arrows
        
    Returns:
        ax: Matplotlib axis with plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    
    # Compute velocities for arrows
    velocities = compute_velocities(headings, config.nu_0)
    
    # Plot particles as points
    ax.scatter(positions[:, 0], positions[:, 1], s=20, c='blue', alpha=0.6)
    
    # Plot velocity arrows
    ax.quiver(positions[:, 0], positions[:, 1], 
              velocities[:, 0], velocities[:, 1],
              scale=config.nu_0 * 10 / arrow_scale, 
              width=0.003, color='red', alpha=0.7)
    
    # Set domain limits
    ax.set_xlim(0, config.L)
    ax.set_ylim(0, config.L)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set