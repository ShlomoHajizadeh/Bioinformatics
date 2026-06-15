"""Visualization functions for Vicsek model."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle
from config import VicsekConfig
from diagnostics import compute_velocities, order_parameter


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
    ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
    
    return ax


def create_animation(trajectory: dict, config: VicsekConfig, 
                    interval: int = 50, skip_frames: int = 1,
                    save_path: str = None, show: bool = True):
    """Create animation of the Vicsek model evolution.
    
    Args:
        trajectory: Dictionary with simulation results
        config: Vicsek configuration parameters
        interval: Delay between frames in milliseconds
        skip_frames: Show every n-th frame (for faster animation)
        save_path: Optional path to save animation as GIF
        show: Whether to display the animation
        
    Returns:
        anim: FuncAnimation object
    """
    # Select frames to animate
    n_frames = len(trajectory['positions'])
    frame_indices = range(0, n_frames, skip_frames)
    
    # Create figure with two subplots
    fig = plt.figure(figsize=(16, 7))
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)
    
    # Initialize plots
    velocities_init = compute_velocities(trajectory['headings'][0], config.nu_0)
    
    # Left plot: particle positions and velocities
    scatter = ax1.scatter(trajectory['positions'][0][:, 0], 
                         trajectory['positions'][0][:, 1], 
                         s=30, c='blue', alpha=0.6)
    quiver = ax1.quiver(trajectory['positions'][0][:, 0], 
                       trajectory['positions'][0][:, 1],
                       velocities_init[:, 0], velocities_init[:, 1],
                       scale=config.nu_0 * 10 / 0.3, 
                       width=0.003, color='red', alpha=0.7)
    
    ax1.set_xlim(0, config.L)
    ax1.set_ylim(0, config.L)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.grid(True, alpha=0.3)
    title1 = ax1.set_title(f'Time: 0.0, Order: {trajectory["order_parameter"][0]:.3f}', 
                          fontsize=14, fontweight='bold')
    
    # Right plot: order parameter evolution
    line, = ax2.plot([], [], linewidth=2.5, color='darkblue')
    ax2.set_xlim(0, trajectory['time'][-1])
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Order Parameter', fontsize=12)
    ax2.set_title('Order Parameter Evolution', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add horizontal reference lines
    ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Vertical line marker for current time
    vline = ax2.axvline(x=0, color='red', linestyle='-', alpha=0.7, linewidth=2)
    
    plt.tight_layout()
    
    def init():
        """Initialize animation."""
        line.set_data([], [])
        return scatter, quiver, line, title1, vline
    
    def update(frame_num):
        """Update animation frame."""
        idx = frame_indices[frame_num]
        
        # Get current state
        positions = trajectory['positions'][idx]
        headings = trajectory['headings'][idx]
        time = trajectory['time'][idx]
        order = trajectory['order_parameter'][idx]
        
        # Update particle positions
        scatter.set_offsets(positions)
        
        # Update velocity arrows
        velocities = compute_velocities(headings, config.nu_0)
        quiver.set_offsets(positions)
        quiver.set_UVC(velocities[:, 0], velocities[:, 1])
        
        # Update title with current time and order parameter
        title1.set_text(f'Time: {time:.1f}, Order: {order:.3f}')
        
        # Update order parameter plot
        times_so_far = trajectory['time'][:idx+1]
        orders_so_far = trajectory['order_parameter'][:idx+1]
        line.set_data(times_so_far, orders_so_far)
        
        # Update vertical line marker
        vline.set_xdata([time, time])
        
        return scatter, quiver, line, title1, vline
    
    # Create animation
    anim = FuncAnimation(fig, update, init_func=init,
                        frames=len(frame_indices), 
                        interval=interval, blit=True)
    
    # Save animation if path provided
    if save_path:
        print(f"Saving animation to {save_path}...")
        writer = PillowWriter(fps=1000//interval)
        anim.save(save_path, writer=writer)
        print(f"Animation saved successfully!")
    
    # Show animation
    if show:
        plt.show()
    
    return anim


def create_simple_animation(trajectory: dict, config: VicsekConfig,
                           interval: int = 50, skip_frames: int = 1,
                           save_path: str = None, show: bool = True):
    """Create simple animation showing only particle evolution.
    
    Args:
        trajectory: Dictionary with simulation results
        config: Vicsek configuration parameters
        interval: Delay between frames in milliseconds
        skip_frames: Show every n-th frame
        save_path: Optional path to save animation as GIF
        show: Whether to display the animation
        
    Returns:
        anim: FuncAnimation object
    """
    # Select frames to animate
    n_frames = len(trajectory['positions'])
    frame_indices = range(0, n_frames, skip_frames)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Initialize plot
    velocities_init = compute_velocities(trajectory['headings'][0], config.nu_0)
    
    scatter = ax.scatter(trajectory['positions'][0][:, 0], 
                        trajectory['positions'][0][:, 1], 
                        s=30, c='blue', alpha=0.6)
    quiver = ax.quiver(trajectory['positions'][0][:, 0], 
                      trajectory['positions'][0][:, 1],
                      velocities_init[:, 0], velocities_init[:, 1],
                      scale=config.nu_0 * 10 / 0.3, 
                      width=0.003, color='red', alpha=0.7)
    
    ax.set_xlim(0, config.L)
    ax.set_ylim(0, config.L)
    ax.set_aspect('equal')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.grid(True, alpha=0.3)
    title = ax.set_title(f'Vicsek Model - Time: 0.0, Order: {trajectory["order_parameter"][0]:.3f}', 
                        fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    def init():
        """Initialize animation."""
        return scatter, quiver, title
    
    def update(frame_num):
        """Update animation frame."""
        idx = frame_indices[frame_num]
        
        # Get current state
        positions = trajectory['positions'][idx]
        headings = trajectory['headings'][idx]
        time = trajectory['time'][idx]
        order = trajectory['order_parameter'][idx]
        
        # Update particle positions
        scatter.set_offsets(positions)
        
        # Update velocity arrows
        velocities = compute_velocities(headings, config.nu_0)
        quiver.set_offsets(positions)
        quiver.set_UVC(velocities[:, 0], velocities[:, 1])
        
        # Update title
        title.set_text(f'Vicsek Model - Time: {time:.1f}, Order: {order:.3f}')
        
        return scatter, quiver, title
    
    # Create animation
    anim = FuncAnimation(fig, update, init_func=init,
                        frames=len(frame_indices), 
                        interval=interval, blit=True)
    
    # Save animation if path provided
    if save_path:
        print(f"Saving animation to {save_path}...")
        writer = PillowWriter(fps=1000//interval)
        anim.save(save_path, writer=writer)
        print(f"Animation saved successfully!")
    
    # Show animation
    if show:
        plt.show()
    
    return anim