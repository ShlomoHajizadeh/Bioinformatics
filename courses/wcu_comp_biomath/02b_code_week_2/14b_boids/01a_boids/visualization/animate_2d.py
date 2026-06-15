"""
2D animation for Reynolds boids simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter


def animate_2d(history, config, filename='boids_2d.gif', fps=30, show=False, use_ffmpeg=False):
    """
    Create an animation of the 2D boids simulation.
    
    Args:
        history: list of State objects
        config: Configuration object
        filename: output filename (.gif or .mp4)
        fps: frames per second
        show: whether to display the animation
        use_ffmpeg: if True, use FFmpeg for MP4, otherwise use Pillow for GIF
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    Lx, Ly = config.domain_size
    
    # Set up plot
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_aspect('equal')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Initialize empty plots
    quiver_sp1 = None
    quiver_sp2 = None
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                       fontsize=12, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def init():
        """Initialize animation."""
        ax.set_title('Reynolds Boids - 2D Animation', fontsize=14, fontweight='bold')
        return []
    
    def update(frame):
        """Update animation frame."""
        nonlocal quiver_sp1, quiver_sp2
        
        state = history[frame]
        positions = state.positions
        velocities = state.velocities
        
        # Clear previous quivers
        if quiver_sp1 is not None:
            quiver_sp1.remove()
        if quiver_sp2 is not None:
            quiver_sp2.remove()
        
        # Separate species
        mask_sp1 = state.get_species_mask(config.species1_label)
        mask_sp2 = state.get_species_mask(config.species2_label)
        
        artists = []
        
        # Plot species 1
        if np.any(mask_sp1):
            pos_sp1 = positions[mask_sp1]
            vel_sp1 = velocities[mask_sp1]
            quiver_sp1 = ax.quiver(pos_sp1[:, 0], pos_sp1[:, 1],
                                   vel_sp1[:, 0], vel_sp1[:, 1],
                                   color='blue', alpha=0.6, scale=20, width=0.003,
                                   label='Species 1')
            artists.append(quiver_sp1)
        
        # Plot species 2
        if np.any(mask_sp2):
            pos_sp2 = positions[mask_sp2]
            vel_sp2 = velocities[mask_sp2]
            quiver_sp2 = ax.quiver(pos_sp2[:, 0], pos_sp2[:, 1],
                                   vel_sp2[:, 0], vel_sp2[:, 1],
                                   color='red', alpha=0.8, scale=20, width=0.004,
                                   label='Species 2')
            artists.append(quiver_sp2)
        
        # Update time text
        time = frame * config.dt * config.save_every
        time_text.set_text(f'Time: {time:.1f}\nFrame: {frame}/{len(history)-1}')
        artists.append(time_text)
        
        return artists
    
    # Create animation
    anim = FuncAnimation(fig, update, init_func=init,
                        frames=len(history), interval=1000/fps,
                        blit=True, repeat=True)
    
    # Save animation
    print(f"Creating animation with {len(history)} frames...")
    
    try:
        if use_ffmpeg or filename.endswith('.mp4'):
            writer = FFMpegWriter(fps=fps, bitrate=2000)
            anim.save(filename, writer=writer)
        else:
            # Use Pillow for GIF (no FFmpeg needed)
            if not filename.endswith('.gif'):
                filename = filename.rsplit('.', 1)[0] + '.gif'
            writer = PillowWriter(fps=fps)
            anim.save(filename, writer=writer)
        print(f"Saved animation to {filename}")
    except FileNotFoundError:
        print("ERROR: FFmpeg not found. Saving as GIF instead...")
        gif_filename = filename.rsplit('.', 1)[0] + '.gif'
        writer = PillowWriter(fps=fps)
        anim.save(gif_filename, writer=writer)
        print(f"Saved animation to {gif_filename}")
    
    if show:
        plt.show()
    else:
        plt.close()