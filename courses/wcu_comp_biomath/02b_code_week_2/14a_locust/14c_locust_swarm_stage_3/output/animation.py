"""
Creates animations of the swarm dynamics.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def create_animation(history_positions, history_grounded, times, 
                    save_path=None, fps=10, interval=50):
    """
    Create an animation of the swarm evolution.
    
    Parameters:
    -----------
    history_positions : list
        List of position arrays
    history_grounded : list
        List of grounded masks
    times : ndarray
        Array of time points
    save_path : str, optional
        Path to save animation (as GIF or MP4)
    fps : int
        Frames per second for saved animation
    interval : int
        Delay between frames in milliseconds
    
    Returns:
    --------
    animation.FuncAnimation
        The animation object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Determine plot limits
    all_positions = np.vstack(history_positions)
    x_min, x_max = all_positions[:, 0].min(), all_positions[:, 0].max()
    z_min, z_max = all_positions[:, 1].min(), all_positions[:, 1].max()
    
    margin = 0.1 * max(x_max - x_min, z_max - z_min)
    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(z_min - margin, z_max + margin)
    
    ax.set_xlabel('x (horizontal)', fontsize=12)
    ax.set_ylabel('z (vertical)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='brown', linestyle='--', linewidth=2)
    ax.set_aspect('equal')
    
    # Initialize scatter plots
    scat_airborne = ax.scatter([], [], c='blue', s=50, alpha=0.6, label='Airborne')
    scat_grounded = ax.scatter([], [], c='red', s=50, alpha=0.6, label='Grounded')
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
    ax.legend()
    
    def init():
        scat_airborne.set_offsets(np.empty((0, 2)))
        scat_grounded.set_offsets(np.empty((0, 2)))
        time_text.set_text('')
        return scat_airborne, scat_grounded, time_text
    
    def update(frame):
        positions = history_positions[frame]
        grounded = history_grounded[frame]
        
        airborne = ~grounded
        
        # Update airborne locusts
        if np.any(airborne):
            scat_airborne.set_offsets(positions[airborne])
        else:
            scat_airborne.set_offsets(np.empty((0, 2)))
        
        # Update grounded locusts
        if np.any(grounded):
            scat_grounded.set_offsets(positions[grounded])
        else:
            scat_grounded.set_offsets(np.empty((0, 2)))
        
        time_text.set_text(f'Time: {times[frame]:.2f}')
        
        return scat_airborne, scat_grounded, time_text
    
    anim = animation.FuncAnimation(fig, update, init_func=init,
                                  frames=len(history_positions),
                                  interval=interval, blit=True)
    
    if save_path:
        if save_path.endswith('.gif'):
            anim.save(save_path, writer='pillow', fps=fps)
            print(f"Animation saved to {save_path}")
        elif save_path.endswith('.mp4'):
            anim.save(save_path, writer='ffmpeg', fps=fps)
            print(f"Animation saved to {save_path}")
    
    return anim