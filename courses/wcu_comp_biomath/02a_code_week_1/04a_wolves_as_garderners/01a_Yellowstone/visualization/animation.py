"""
Animation creation for simulation visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap
import os
from config.config import OUTPUT_DIR, CELL_TYPE_FOREST, CELL_TYPE_GRASS


def create_animation(sim, filename='simulation.gif', fps=10):
    """
    Create animated GIF of simulation progression.
    
    Args:
        sim: Simulation object (must have state_history)
        filename: Output filename
        fps: Frames per second
    """
    if not hasattr(sim, 'state_history') or len(sim.state_history) == 0:
        print("Error: No state history found. Run simulation with save_history=True")
        print("Example: sim.run(n_steps=500, save_history=True, history_interval=5)")
        return
    
    print(f"Creating animation from {len(sim.state_history)} frames...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    def update(frame_idx):
        state = sim.state_history[frame_idx]
        
        for ax in axes.flat:
            ax.clear()
        
        cell_types = state['cell_types']
        grass_stages = state['grass_stages']
        bison_count = state['bison_count']
        wolf_count = state['wolf_count']
        
        # Cell types
        ax = axes[0, 0]
        cell_type_numeric = np.where(cell_types == CELL_TYPE_FOREST, 1, 0)
        im = ax.imshow(cell_type_numeric, cmap=ListedColormap(['lightgreen', 'darkgreen']), 
                       origin='lower', interpolation='nearest')
        ax.set_title(f'Cell Types (Step {state["step"]})', fontweight='bold')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # Grass stages
        ax = axes[0, 1]
        grass_display = np.where(cell_types == CELL_TYPE_GRASS, grass_stages, np.nan)
        im = ax.imshow(grass_display, cmap='YlGn', origin='lower', 
                       interpolation='nearest', vmin=0, vmax=10)
        ax.set_title('Grass Stages (0-10)', fontweight='bold')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # Bison
        ax = axes[1, 0]
        im = ax.imshow(bison_count, cmap='Blues', origin='lower', interpolation='nearest')
        ax.set_title(f'Bison Distribution (n={state["n_bison"]})', fontweight='bold')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # Wolves
        ax = axes[1, 1]
        im = ax.imshow(wolf_count, cmap='Reds', origin='lower', interpolation='nearest')
        ax.set_title(f'Wolf Distribution (n={state["n_wolves"]})', fontweight='bold')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        plt.tight_layout()
    
    anim = FuncAnimation(fig, update, frames=len(sim.state_history), 
                         interval=1000/fps, repeat=True)
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    try:
        writer = PillowWriter(fps=fps)
        anim.save(filepath, writer=writer)
        print(f"✓ Animation saved: {filepath}")
    except Exception as e:
        print(f"Error saving animation: {e}")
        print("Saving as MP4 instead...")
        filepath_mp4 = filepath.replace('.gif', '.mp4')
        anim.save(filepath_mp4, writer='ffmpeg', fps=fps)
        print(f"✓ Animation saved: {filepath_mp4}")
    
    plt.close()