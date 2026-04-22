"""
Visualization functions for simulation state and statistics.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
from config.config import OUTPUT_DIR, CELL_TYPE_FOREST, CELL_TYPE_GRASS


def plot_combined_state(sim, filename=None):
    """
    Create combined visualization of current simulation state.
    
    Args:
        sim: Simulation object
        filename: Output filename (if None, display instead of save)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Get current state
    state = sim.get_current_state()
    cell_types = state['cell_types']
    grass_stages = state['grass_stages']
    bison_count = state['bison_count']
    wolf_count = state['wolf_count']
    
    # 1. Cell types (forest/grassland)
    ax = axes[0, 0]
    cell_type_numeric = np.where(cell_types == CELL_TYPE_FOREST, 1, 0)
    im1 = ax.imshow(cell_type_numeric, cmap=ListedColormap(['lightgreen', 'darkgreen']), 
                    origin='lower', interpolation='nearest')
    ax.set_title(f'Cell Types (Step {state["step"]})', fontsize=12, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    cbar1 = plt.colorbar(im1, ax=ax, ticks=[0, 1])
    cbar1.set_ticklabels(['Grassland', 'Forest'])
    
    # 2. Grass stages
    ax = axes[0, 1]
    grass_display = np.where(cell_types == CELL_TYPE_GRASS, grass_stages, np.nan)
    im2 = ax.imshow(grass_display, cmap='YlGn', origin='lower', 
                    interpolation='nearest', vmin=0, vmax=10)
    ax.set_title('Grass Stages (0-10)', fontsize=12, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    cbar2 = plt.colorbar(im2, ax=ax)
    cbar2.set_label('Stage')
    
    # 3. Bison distribution
    ax = axes[1, 0]
    im3 = ax.imshow(bison_count, cmap='Blues', origin='lower', 
                    interpolation='nearest', vmin=0)
    ax.set_title(f'Bison Distribution (Total: {len(sim.bison)})', 
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    cbar3 = plt.colorbar(im3, ax=ax)
    cbar3.set_label('Count')
    
    # 4. Wolf distribution
    ax = axes[1, 1]
    im4 = ax.imshow(wolf_count, cmap='Reds', origin='lower', 
                    interpolation='nearest', vmin=0)
    ax.set_title(f'Wolf Distribution (Total: {len(sim.wolves)})', 
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    cbar4 = plt.colorbar(im4, ax=ax)
    cbar4.set_label('Count')
    
    plt.tight_layout()
    
    if filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved: {filepath}")
        plt.close()
    else:
        plt.show()


def plot_time_series(sim, filename=None):
    """
    Plot time series of key statistics.
    
    Args:
        sim: Simulation object
        filename: Output filename (if None, display instead of save)
    """
    stats = sim.statistics
    
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    
    # 1. Forest and grassland cells
    ax = axes[0, 0]
    ax.plot(stats['step'], stats['forest_cells'], 'g-', label='Forest', linewidth=2)
    ax.plot(stats['step'], stats['grassland_cells'], 'y-', label='Grassland', linewidth=2)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Number of Cells')
    ax.set_title('Land Cover', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Mean grass stage
    ax = axes[0, 1]
    ax.plot(stats['step'], stats['mean_grass_stage'], 'g-', linewidth=2)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Mean Stage')
    ax.set_title('Mean Grass Stage', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=4, color='r', linestyle='--', alpha=0.5, label='Preference threshold')
    ax.legend()
    
    # 3. Overgrazed and stage 10 cells
    ax = axes[1, 0]
    ax.plot(stats['step'], stats['overgrazed_cells'], 'r-', label='Overgrazed (stage 0)', linewidth=2)
    ax.plot(stats['step'], stats['stage10_cells'], 'b-', label='Stage 10', linewidth=2)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Number of Cells')
    ax.set_title('Extreme Grass Stages', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Wolf-bison encounters
    ax = axes[1, 1]
    ax.plot(stats['step'], stats['wolf_bison_encounters'], 'purple', linewidth=2)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Number of Encounter Cells')
    ax.set_title('Wolf-Bison Encounters', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # 5. Bison movement statistics
    ax = axes[2, 0]
    ax.plot(stats['step'], stats['bison_escaped'], 'r-', label='Escaped from wolves', linewidth=1.5)
    ax.plot(stats['step'], stats['bison_grazed'], 'g-', label='Grazing moves', linewidth=1.5)
    ax.plot(stats['step'], stats['bison_resolved'], 'b-', label='Social resolutions', linewidth=1.5)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Number of Moves')
    ax.set_title('Bison Movement Events', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 6. Cumulative forest conversions
    ax = axes[2, 1]
    cumulative_conversions = np.cumsum(stats['forest_conversions'])
    ax.plot(stats['step'], cumulative_conversions, 'darkgreen', linewidth=2)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Cumulative Conversions')
    ax.set_title('Cumulative Forest Conversions', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved: {filepath}")
        plt.close()
    else:
        plt.show()


def plot_spatial_heatmap(sim, variable='grass_stages', filename=None):
    """
    Plot spatial heatmap of a specific variable.
    
    Args:
        sim: Simulation object
        variable: Variable to plot ('grass_stages', 'bison_count', 'wolf_count')
        filename: Output filename (if None, display instead of save)
    """
    state = sim.get_current_state()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if variable == 'grass_stages':
        data = state['grass_stages']
        cmap = 'YlGn'
        title = 'Grass Stages'
        vmin, vmax = 0, 10
    elif variable == 'bison_count':
        data = state['bison_count']
        cmap = 'Blues'
        title = 'Bison Count'
        vmin, vmax = 0, None
    elif variable == 'wolf_count':
        data = state['wolf_count']
        cmap = 'Reds'
        title = 'Wolf Count'
        vmin, vmax = 0, None
    else:
        raise ValueError(f"Unknown variable: {variable}")
    
    im = ax.imshow(data, cmap=cmap, origin='lower', interpolation='nearest',
                   vmin=vmin, vmax=vmax)
    ax.set_title(f'{title} (Step {state["step"]})', fontsize=14, fontweight='bold')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.colorbar(im, ax=ax, label=title)
    
    plt.tight_layout()
    
    if filename:
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved: {filepath}")
        plt.close()
    else:
        plt.show()