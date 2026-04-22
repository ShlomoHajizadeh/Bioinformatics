"""Visualization functions for the Vicsek model."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from config import VicsekConfig


def plot_state(positions: np.ndarray, headings: np.ndarray, 
               config: VicsekConfig, ax=None, show_velocities: bool = True):
    """Plot the current state of the Vicsek model.
    
    Args:
        positions: Particle positions of shape (N, 2)
        headings: Particle headings of shape (N,)
        config: Vicsek configuration
        ax: Matplotlib axis (creates new figure if None)
        show_velocities: Whether to show velocity arrows
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot domain boundaries
    ax.set_xlim(0, config.L)
    ax.set_ylim(0, config.L)
    ax.set_aspect('equal')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    
    # Draw obstacle if present
    if config.obstacle_center is not None:
        obstacle = Circle(
            config.obstacle_center, 
            config.obstacle_radius, 
            color='green', 
            alpha=0.6,
            zorder=1,
            label='Obstacle'
        )
        ax.add_patch(obstacle)
    
    # Plot particles
    ax.scatter(positions[:, 0], positions[:, 1], 
              c='blue', s=30, alpha=0.6, zorder=2)
    
    # Plot velocity arrows
    if show_velocities:
        scale = 0.3  # Arrow length scale
        dx = scale * np.cos(headings)
        dy = scale * np.sin(headings)
        ax.quiver(positions[:, 0], positions[:, 1], dx, dy,
                 color='red', alpha=0.7, width=0.003, 
                 scale=1, scale_units='xy', zorder=3)
    
    ax.grid(True, alpha=0.3)
    
    if config.obstacle_center is not None:
        ax.legend(loc='upper right')
    
    return ax


def create_animation(trajectory: dict, config: VicsekConfig,
                    interval: int = 50, skip_frames: int = 1,
                    save_path: str = None, show: bool = True):
    """Create animation of the Vicsek model simulation.
    
    Args:
        trajectory: Dictionary with 'positions', 'headings', 'order_parameter', 'time'
        config: Vicsek configuration
        interval: Milliseconds between frames
        skip_frames: Show every nth frame
        save_path: Path to save animation (if provided)
        show: Whether to display the animation
        
    Returns:
        anim: Animation object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Setup main plot
    ax1.set_xlim(0, config.L)
    ax1.set_ylim(0, config.L)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Draw obstacle if present (static)
    if config.obstacle_center is not None:
        obstacle = Circle(
            config.obstacle_center, 
            config.obstacle_radius, 
            color='green', 
            alpha=0.6,
            zorder=1
        )
        ax1.add_patch(obstacle)
    
    # Initialize particle plot
    particles = ax1.scatter([], [], c='blue', s=30, alpha=0.6, zorder=2)
    
    # Initialize quiver with first frame data to avoid empty quiver issues
    pos0 = trajectory['positions'][0]
    head0 = trajectory['headings'][0]
    scale = 0.3
    dx0 = scale * np.cos(head0)
    dy0 = scale * np.sin(head0)
    quiver = ax1.quiver(pos0[:, 0], pos0[:, 1], dx0, dy0,
                       color='red', alpha=0.7, width=0.003, 
                       scale=1, scale_units='xy', zorder=3)
    
    title1 = ax1.set_title('', fontsize=14, fontweight='bold')
    
    # Setup order parameter plot
    ax2.set_xlim(0, trajectory['time'][-1])
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Order Parameter', fontsize=12)
    ax2.set_title('Order Parameter Evolution', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    line, = ax2.plot([], [], linewidth=2, color='darkblue')
    
    # Add vertical line for current time position
    time_marker = ax2.axvline(x=0, color='red', linewidth=2, linestyle='-', alpha=0.7)
    
    # Select frames to show
    frames = range(0, len(trajectory['positions']), skip_frames)
    
    def init():
        particles.set_offsets(pos0)
        line.set_data([], [])
        time_marker.set_xdata([0])
        return particles, quiver, line, title1, time_marker
    
    def update(frame_idx):
        frame = frames[frame_idx]
        
        # Update particles
        pos = trajectory['positions'][frame]
        head = trajectory['headings'][frame]
        
        particles.set_offsets(pos)
        
        # Update velocity arrows
        scale = 0.3
        dx = scale * np.cos(head)
        dy = scale * np.sin(head)
        
        # Update quiver by setting new positions and vectors
        quiver.set_offsets(pos)
        quiver.set_UVC(dx, dy)
        
        # Update title
        t = trajectory['time'][frame]
        order = trajectory['order_parameter'][frame]
        title1.set_text(f'Time: {t:.1f}, Order: {order:.3f}')
        
        # Update order parameter plot
        times = trajectory['time'][:frame+1]
        orders = trajectory['order_parameter'][:frame+1]
        line.set_data(times, orders)
        
        # Update time marker position
        time_marker.set_xdata([t])
        
        return particles, quiver, line, title1, time_marker
    
    anim = FuncAnimation(fig, update, init_func=init, 
                        frames=len(frames), interval=interval,
                        blit=True, repeat=True)
    
    plt.tight_layout()
    
    if save_path:
        print(f"Saving animation to {save_path}...")
        anim.save(save_path, writer='pillow', fps=20)
        print(f"Animation saved!")
    
    if show:
        plt.show()
    
    return anim


def create_simple_animation(trajectory: dict, config: VicsekConfig,
                           interval: int = 50, skip_frames: int = 1,
                           save_path: str = None, show: bool = True):
    """Create simple animation showing only particles.
    
    Args:
        trajectory: Dictionary with 'positions', 'headings', 'time'
        config: Vicsek configuration
        interval: Milliseconds between frames
        skip_frames: Show every nth frame
        save_path: Path to save animation (if provided)
        show: Whether to display the animation
        
    Returns:
        anim: Animation object
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Setup plot
    ax.set_xlim(0, config.L)
    ax.set_ylim(0, config.L)
    ax.set_aspect('equal')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Draw obstacle if present (static)
    if config.obstacle_center is not None:
        obstacle = Circle(
            config.obstacle_center, 
            config.obstacle_radius, 
            color='green', 
            alpha=0.6,
            zorder=1
        )
        ax.add_patch(obstacle)
    
    # Initialize particle plot
    particles = ax.scatter([], [], c='blue', s=30, alpha=0.6, zorder=2)
    
    # Initialize quiver with first frame data
    pos0 = trajectory['positions'][0]
    head0 = trajectory['headings'][0]
    scale = 0.3
    dx0 = scale * np.cos(head0)
    dy0 = scale * np.sin(head0)
    quiver = ax.quiver(pos0[:, 0], pos0[:, 1], dx0, dy0,
                       color='red', alpha=0.7, width=0.003, 
                       scale=1, scale_units='xy', zorder=3)
    
    title = ax.set_title('', fontsize=14, fontweight='bold')
    
    # Select frames to show
    frames = range(0, len(trajectory['positions']), skip_frames)
    
    def init():
        particles.set_offsets(pos0)
        return particles, quiver, title
    
    def update(frame_idx):
        frame = frames[frame_idx]
        
        # Update particles
        pos = trajectory['positions'][frame]
        head = trajectory['headings'][frame]
        
        particles.set_offsets(pos)
        
        # Update velocity arrows
        scale = 0.3
        dx = scale * np.cos(head)
        dy = scale * np.sin(head)
        quiver.set_offsets(pos)
        quiver.set_UVC(dx, dy)
        
        # Update title
        t = trajectory['time'][frame]
        title.set_text(f'Time: {t:.1f}')
        
        return particles, quiver, title
    
    anim = FuncAnimation(fig, update, init_func=init, 
                        frames=len(frames), interval=interval,
                        blit=True, repeat=True)
    
    plt.tight_layout()
    
    if save_path:
        print(f"Saving animation to {save_path}...")
        anim.save(save_path, writer='pillow', fps=20)
        print(f"Animation saved!")
    
    if show:
        plt.show()
    
    return anim