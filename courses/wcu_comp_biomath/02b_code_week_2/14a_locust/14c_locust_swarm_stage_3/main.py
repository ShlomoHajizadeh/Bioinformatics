"""
Main script to run the Stage 3 locust swarm simulation.
Stage 3: Add wind for rolling/marching swarm behavior.
"""

import numpy as np
import matplotlib.pyplot as plt
from config.parameters import *
from simulation.initializer import (random_cloud, disk_swarm, 
                                   airborne_cloud, airborne_disk)
from simulation.runner import run_simulation
from output.plots import (plot_swarm_snapshot, plot_trajectories, 
                         plot_diagnostics, plot_landing_analysis,
                         plot_rolling_analysis)
from output.animation import create_animation

def main():
    """
    Run Stage 3 simulation: Social swarm with gravity, ground, and wind.
    """
    print("=" * 60)
    print("LOCUST SWARM SIMULATION - STAGE 3")
    print("Social swarm with gravity, ground, and wind (rolling)")
    print("=" * 60)
    print(f"Number of locusts: {N}")
    print(f"Social interaction: F = {F}, L = {L}")
    
    # Determine regime
    if F < 1 and L > 1:
        if L < F**(-1/3):
            regime = "H-stable (crystalline structure expected)"
        else:
            regime = "Catastrophic (bubble structure expected)"
        print(f"  → {regime}")
    
    print(f"Gravity: G = {G}")
    print(f"Wind: U = {U} (ENABLED for rolling behavior)")
    print(f"Time step: {dt}, Total time: {T_total}")
    print("=" * 60)
    
    # Initialize swarm
    print("\nInitializing swarm...")
    print("Using: airborne_cloud initialization")
    
    # Choose one of these initialization methods:
    
    # Option 1: Random cloud (all above ground)
    # state = random_cloud(N, domain_size, seed=random_seed)
    
    # Option 2: Disk swarm (circular, all above ground)
    # state = disk_swarm(N, domain_size/2, seed=random_seed)
    
    # Option 3: Airborne cloud (recommended for Stage 3) ✓
    state = airborne_cloud(N, domain_size, initial_height, seed=random_seed)
    
    # Option 4: Airborne disk (circular cloud at specific height)
    # state = airborne_disk(N, domain_size/3, initial_height, seed=random_seed)
    
    # Verify no negative z-coordinates
    min_z = np.min(state.positions[:, 1])
    max_z = np.max(state.positions[:, 1])
    mean_z = np.mean(state.positions[:, 1])
    print(f"Initial z-coordinates: min={min_z:.3f}, mean={mean_z:.3f}, max={max_z:.3f}")
    
    if min_z < 0:
        print("⚠ WARNING: Some particles initialized below ground! Fixing...")
        state.positions[:, 1] = np.maximum(state.positions[:, 1], 0.1)
        min_z = np.min(state.positions[:, 1])
        print(f"✓ Corrected: all particles now at z ≥ {min_z:.3f}")
    else:
        print("✓ All particles correctly initialized above ground")
    
    # Run simulation
    print("\nRunning simulation...")
    print("Progress: ", end='', flush=True)
    
    results = run_simulation(state, dt, T_total, F, L, G, U)
    
    print("Done!")
    print(f"Simulation complete! ({len(results['times'])} time steps)")
    
    # Extract results
    history_positions = results['history_positions']
    history_grounded = results['history_grounded']
    times = results['times']
    diagnostics = results['diagnostics']
    
    # Summary statistics
    final_grounded = diagnostics['grounded_count'][-1]
    max_grounded = max(diagnostics['grounded_count'])
    final_mean_height = diagnostics['mean_height'][-1]
    
    print("\n" + "=" * 60)
    print("SIMULATION SUMMARY")
    print("=" * 60)
    print(f"Final state: {final_grounded}/{N} locusts grounded ({100*final_grounded/N:.1f}%)")
    print(f"Maximum grounded during simulation: {max_grounded}/{N}")
    print(f"Final mean height: {final_mean_height:.3f}")
    print(f"Final swarm width: {diagnostics['width'][-1]:.3f}")
    print(f"Final swarm height: {diagnostics['height'][-1]:.3f}")
    
    # Stage 3 specific: Rolling statistics
    final_rolling_speed = diagnostics['mean_rolling_speed'][-1]
    final_swarm_length = diagnostics['swarm_length'][-1]
    total_distance = diagnostics['front_position'][-1] - diagnostics['front_position'][0]
    
    print(f"\nRolling behavior:")
    print(f"  Final rolling speed: {final_rolling_speed:.3f}")
    print(f"  Final swarm length: {final_swarm_length:.3f}")
    print(f"  Total distance traveled: {total_distance:.3f}")
    
    # Check for bubble formation
    if final_grounded > N * 0.3 and final_mean_height > 0.5:
        print("\n→ Bubble structure detected (grounded layer + airborne group)")
    elif final_grounded == N:
        print("\n→ All locusts landed (crystalline structure on ground)")
    else:
        print("\n→ Mixed state")
    print("=" * 60)
    
    # Plot initial and final states
    print("\nGenerating plots...")
    
    fig1, _ = plot_swarm_snapshot(history_positions[0], history_grounded[0], 
                                  times[0], "Initial Swarm State - Stage 3")
    plt.savefig('stage3_initial_state.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: stage3_initial_state.png")
    
    fig2, _ = plot_swarm_snapshot(history_positions[-1], history_grounded[-1], 
                                  times[-1], "Final Swarm State - Stage 3")
    plt.savefig('stage3_final_state.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: stage3_final_state.png")
    
    # Plot intermediate state (mid-simulation)
    mid_idx = len(history_positions) // 2
    fig3, _ = plot_swarm_snapshot(history_positions[mid_idx], history_grounded[mid_idx], 
                                  times[mid_idx], "Intermediate State - Stage 3")
    plt.savefig('stage3_intermediate_state.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: stage3_intermediate_state.png")
    
    # Plot trajectories
    fig4, _ = plot_trajectories(history_positions, sample_indices=range(min(N, 15)))
    plt.savefig('stage3_trajectories.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: stage3_trajectories.png")
    
    # Plot diagnostics
    fig5, _ = plot_diagnostics(times, diagnostics)
    plt.savefig('stage3_diagnostics.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: stage3_diagnostics.png")
    
    # Plot landing analysis
    fig6, _ = plot_landing_analysis(times, diagnostics)
    plt.savefig('stage3_landing_analysis.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: stage3_landing_analysis.png")
    
    # Plot rolling analysis
    fig7, _ = plot_rolling_analysis(times, diagnostics)
    plt.savefig('stage3_rolling_analysis.png', dpi=150, bbox_inches='tight')
    print("  ✓ Saved: stage3_rolling_analysis.png")
    
    # Create animation
    if save_animation:
        print("\nCreating animation (this may take a moment)...")
        # Subsample frames for faster animation
        skip = max(1, len(history_positions) // 200)
        anim = create_animation(
            history_positions[::skip],
            history_grounded[::skip],
            times[::skip],
            save_path='stage3_swarm_animation.gif',
            fps=animation_fps
        )
        print("  ✓ Saved: stage3_swarm_animation.gif")
    
    # Show plots interactively
    print("\nDisplaying plots...")
    plt.show()
    
    print("\n" + "=" * 60)
    print("STAGE 3 SIMULATION COMPLETE!")
    print("=" * 60)
    print("\nKey observations to check:")
    print("  1. Is the swarm marching or rolling due to wind?")
    print("  2. Observe rolling dynamics and swarm elongation")
    print("  3. Check final configuration on ground")
    print("=" * 60)


if __name__ == "__main__":
    main()