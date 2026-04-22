"""
Main script to run the Stage 1 locust swarm simulation.
Stage 1: Free-space social swarm (no gravity, no wind).
"""

import numpy as np
import matplotlib.pyplot as plt
from config.parameters import *
from simulation.initializer import random_cloud, disk_swarm
from simulation.runner import run_simulation
from output.plots import plot_swarm_snapshot, plot_trajectories, plot_diagnostics
from output.animation import create_animation

def main():
    """
    Run Stage 1 simulation: Free-space social swarm.
    """
    print("=" * 60)
    print("LOCUST SWARM SIMULATION - STAGE 1")
    print("Free-space social swarm (no gravity, no wind)")
    print("=" * 60)
    print(f"Number of locusts: {N}")
    print(f"Social interaction: F = {F}, L = {L}")
    print(f"Time step: {dt}, Total time: {T_total}")
    print("=" * 60)
    
    # Initialize swarm
    print("\nInitializing swarm...")
    state = random_cloud(N, domain_size, seed=random_seed)
    # Alternative: state = disk_swarm(N, domain_size/2, seed=random_seed)
    
    # Run simulation
    print("Running simulation...")
    results = run_simulation(state, dt, T_total, F, L, G, U)
    
    print(f"Simulation complete! ({len(results['times'])} time steps)")
    
    # Extract results
    history_positions = results['history_positions']
    history_grounded = results['history_grounded']
    times = results['times']
    diagnostics = results['diagnostics']
    
    # Plot initial and final states
    print("\nGenerating plots...")
    
    fig1, _ = plot_swarm_snapshot(history_positions[0], history_grounded[0], 
                                  times[0], "Initial Swarm State")
    plt.savefig('output_initial_state.png', dpi=150, bbox_inches='tight')
    
    fig2, _ = plot_swarm_snapshot(history_positions[-1], history_grounded[-1], 
                                  times[-1], "Final Swarm State")
    plt.savefig('output_final_state.png', dpi=150, bbox_inches='tight')
    
    # Plot trajectories
    fig3, _ = plot_trajectories(history_positions, sample_indices=range(min(N, 20)))
    plt.savefig('output_trajectories.png', dpi=150, bbox_inches='tight')
    
    # Plot diagnostics
    fig4, _ = plot_diagnostics(times, diagnostics)
    plt.savefig('output_diagnostics.png', dpi=150, bbox_inches='tight')
    
    print("Plots saved!")
    
    # Create animation
    if save_animation:
        print("\nCreating animation...")
        # Subsample frames for faster animation
        skip = max(1, len(history_positions) // 200)
        anim = create_animation(
            history_positions[::skip],
            history_grounded[::skip],
            times[::skip],
            save_path='output_swarm_animation.gif',
            fps=animation_fps
        )
    
    # Show plots
    plt.show()
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE!")
    print("=" * 60)


# This is the critical part that was missing!
if __name__ == "__main__":
    main()