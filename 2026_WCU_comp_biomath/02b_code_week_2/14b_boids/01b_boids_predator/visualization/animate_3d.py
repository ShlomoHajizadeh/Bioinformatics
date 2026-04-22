"""
3D animation for Reynolds boids simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter


def animate_3d(history, config, filename='boids_3d.gif', fps=30, show=False, rotate=True, use_ffmpeg=False):
    """
    Create an animation of the 3D boids simulation.
    
    Args:
        history: list of State objects
        config: Configuration object
        filename: output filename (.gif or .mp4)
        fps: frames per second
        show: whether to display the animation
        rotate: whether to rotate the view during animation
        use_ffmpeg: if True, use FFmpeg for MP4, otherwise use Pillow for GIF
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    Lx, Ly, Lz = config.domain_size
    
    # Set up plot
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_zlim(0, Lz)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Initialize containers
    quiver_sp1 = None
    quiver_sp2 = None
    time_text = ax.text2D(0.02, 0.98, '', transform=ax.transAxes,
                         fontsize=12, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def init():
        """Initialize animation."""
        ax.set_title('Reynolds Boids - 3D Animation', fontsize=14, fontweight='bold')
        ax.view_init(elev=30, azim=45)
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
            quiver_sp1 = ax.quiver(pos_sp1[:, 0], pos_sp1[:, 1], pos_sp1[:, 2],
                                   vel_sp1[:, 0], vel_sp1[:, 1], vel_sp1[:, 2],
                                   color='blue', alpha=0.6, length=2, normalize=True,
                                   arrow_length_ratio=0.3)
            artists.append(quiver_sp1)
        
        # Plot species 2
        if np.any(mask_sp2):
            pos_sp2 = positions[mask_sp2]
            vel_sp2 = velocities[mask_sp2]
            quiver_sp2 = ax.quiver(pos_sp2[:, 0], pos_sp2[:, 1], pos_sp2[:, 2],
                                   vel_sp2[:, 0], vel_sp2[:, 1], vel_sp2[:, 2],
                                   color='red', alpha=0.8, length=2, normalize=True,
                                   arrow_length_ratio=0.3)
            artists.append(quiver_sp2)
        
        # Rotate view if requested
        if rotate:
            azim = 45 + (frame * 360 / len(history))
            ax.view_init(elev=30, azim=azim)
        
        # Update time text
        time = frame * config.dt * config.save_every
        time_text.set_text(f'Time: {time:.1f}\nFrame: {frame}/{len(history)-1}')
        artists.append(time_text)
        
        return artists
    
    # Create animation
    anim = FuncAnimation(fig, update, init_func=init,
                        frames=len(history), interval=1000/fps,
                        blit=False, repeat=True)
    
    # Save animation
    print(f"Creating 3D animation with {len(history)} frames...")
    
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


def animate_3d_with_trails(history, config, filename='boids_3d_trails.gif', 
                          fps=30, trail_length=20):
    """
    Create 3D animation with trajectory trails.
    
    Args:
        history: list of State objects
        config: Configuration object
        filename: output filename
        fps: frames per second
        trail_length: number of past positions to show
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    Lx, Ly, Lz = config.domain_size
    
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_zlim(0, Lz)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_title('Reynolds Boids - 3D with Trails', fontsize=14, fontweight='bold')
    
    scatter_sp1 = None
    scatter_sp2 = None
    trail_lines = []
    
    def init():
        """Initialize animation."""
        ax.view_init(elev=30, azim=45)
        return []
    
    def update(frame):
        """Update animation frame."""
        nonlocal scatter_sp1, scatter_sp2, trail_lines
        
        state = history[frame]
        positions = state.positions
        
        # Clear previous artists
        if scatter_sp1 is not None:
            scatter_sp1.remove()
        if scatter_sp2 is not None:
            scatter_sp2.remove()
        for line in trail_lines:
            line.remove()
        trail_lines = []
        
        # Separate species
        mask_sp1 = state.get_species_mask(config.species1_label)
        mask_sp2 = state.get_species_mask(config.species2_label)
        
        artists = []
        
        # Plot current positions
        if np.any(mask_sp1):
            pos_sp1 = positions[mask_sp1]
            scatter_sp1 = ax.scatter(pos_sp1[:, 0], pos_sp1[:, 1], pos_sp1[:, 2],
                                    c='blue', s=50, alpha=0.8, marker='o')
            artists.append(scatter_sp1)
        
        if np.any(mask_sp2):
            pos_sp2 = positions[mask_sp2]
            scatter_sp2 = ax.scatter(pos_sp2[:, 0], pos_sp2[:, 1], pos_sp2[:, 2],
                                    c='red', s=60, alpha=0.8, marker='^')
            artists.append(scatter_sp2)
        
        # Draw trails
        start_frame = max(0, frame - trail_length)
        if frame > 0:
            # Sample a few agents to show trails
            n_trail_agents = min(10, state.n_agents)
            trail_indices = np.linspace(0, state.n_agents - 1, n_trail_agents, dtype=int)
            
            for idx in trail_indices:
                trail_positions = []
                for f in range(start_frame, frame + 1):
                    trail_positions.append(history[f].positions[idx])
                trail_positions = np.array(trail_positions)
                
                # Determine color based on species
                color = 'blue' if state.species[idx] == config.species1_label else 'red'
                
                line, = ax.plot(trail_positions[:, 0], 
                               trail_positions[:, 1], 
                               trail_positions[:, 2],
                               color=color, alpha=0.3, linewidth=1)
                trail_lines.append(line)
                artists.append(line)
        
        # Rotate view
        azim = 45 + (frame * 360 / len(history))
        ax.view_init(elev=30, azim=azim)
        
        return artists
    
    # Create animation
    anim = FuncAnimation(fig, update, init_func=init,
                        frames=len(history), interval=1000/fps,
                        blit=False, repeat=True)
    
    # Save animation
    print(f"Creating 3D animation with trails ({len(history)} frames)...")
    
    try:
        if filename.endswith('.mp4'):
            writer = FFMpegWriter(fps=fps, bitrate=2000)
        else:
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
    
    plt.close()


def animate_3d_simple(history, config, filename='boids_3d_simple.gif', fps=30):
    """
    Simple 3D animation using scatter plots (faster rendering).
    
    Args:
        history: list of State objects
        config: Configuration object
        filename: output filename
        fps: frames per second
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    Lx, Ly, Lz = config.domain_size
    
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_zlim(0, Lz)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('Reynolds Boids - 3D', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.view_init(elev=30, azim=45)
    
    scatter_sp1 = None
    scatter_sp2 = None
    time_text = ax.text2D(0.02, 0.98, '', transform=ax.transAxes,
                         fontsize=12, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def update(frame):
        """Update animation frame."""
        nonlocal scatter_sp1, scatter_sp2
        
        state = history[frame]
        positions = state.positions
        
        # Clear previous scatter plots
        if scatter_sp1 is not None:
            scatter_sp1.remove()
        if scatter_sp2 is not None:
            scatter_sp2.remove()
        
        mask_sp1 = state.get_species_mask(config.species1_label)
        mask_sp2 = state.get_species_mask(config.species2_label)
        
        artists = []
        
        if np.any(mask_sp1):
            pos_sp1 = positions[mask_sp1]
            scatter_sp1 = ax.scatter(pos_sp1[:, 0], pos_sp1[:, 1], pos_sp1[:, 2],
                                    c='blue', s=30, alpha=0.6, label='Species 1')
            artists.append(scatter_sp1)
        
        if np.any(mask_sp2):
            pos_sp2 = positions[mask_sp2]
            scatter_sp2 = ax.scatter(pos_sp2[:, 0], pos_sp2[:, 1], pos_sp2[:, 2],
                                    c='red', s=40, alpha=0.8, label='Species 2')
            artists.append(scatter_sp2)
        
        # Update time
        time = frame * config.dt * config.save_every
        time_text.set_text(f'Time: {time:.1f}\nFrame: {frame}/{len(history)-1}')
        artists.append(time_text)
        
        return artists
    
    anim = FuncAnimation(fig, update, frames=len(history), 
                        interval=1000/fps, blit=False, repeat=True)
    
    print(f"Creating simple 3D animation with {len(history)} frames...")
    
    try:
        if filename.endswith('.mp4'):
            writer = FFMpegWriter(fps=fps, bitrate=2000)
        else:
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
    
    plt.close()