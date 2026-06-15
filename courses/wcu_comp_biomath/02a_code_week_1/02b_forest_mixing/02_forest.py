"""
forest.py

Main entry point for the stochastic forest model simulation with Moore neighborhood.

This script configures and runs the forest simulation with the following features:
- Moore neighborhood (8-cell) spatial interactions
- Periodic boundary conditions
- Two-plantation initial condition (upper half HI, lower half RO)
- Modular design for easy extension
- Configurable parameters
- Visualization of results
- Statistical output
"""

import numpy as np
from P02_initialization import create_half_split_lattice, create_random_lattice
from P02_dynamics import run_simulation
from P01_visualization import (plot_lattice, plot_time_series, 
                           create_animation, print_statistics)


def main():
    """
    Main function to configure and run the forest simulation.
    """
    
    # ===================================================================
    # CONFIGURATION PARAMETERS
    # ===================================================================
    
    # Lattice size (N x N grid)
    N = 100
    
    # Number of time steps
    T = 100
    
    # Random seed for reproducibility (set to None for random results)
    SEED = 42
    
    # Transition probabilities (used when NOT all neighbors are same species)
    # Format: {state: [P(->RO), P(->HI)]}
    # State 0 = Red Oak (RO), State 1 = Hickory (HI)
    #
    # Special rule: If all 8 neighbors match the current cell state,
    #               the cell stays in that state with probability 1.0
    transition_probabilities = {
        0: [0.50, 0.50],  # RO -> RO with 50%, RO -> HI with 50% (when mixed neighbors)
        1: [0.74, 0.26]   # HI -> RO with 74%, HI -> HI with 26% (when mixed neighbors)
    }
    
    # Visualization options
    save_animation = True   # Set to False to skip animation (saves time)
    show_plots = True       # Set to False to only save plots without displaying
    animation_interval = 100  # Milliseconds between frames
    
    # ===================================================================
    # INITIALIZATION
    # ===================================================================
    
    print("="*70)
    print("STOCHASTIC FOREST MODEL SIMULATION - MOORE NEIGHBORHOOD")
    print("="*70)
    print(f"Lattice size: {N} x {N}")
    print(f"Time steps: {T}")
    print(f"Random seed: {SEED}")
    print(f"Boundary condition: PERIODIC (torus topology)")
    print(f"Neighborhood: Moore (8 cells)")
    print(f"\nInitial condition: Two-plantation setup")
    print(f"  Upper half (rows 0-{N//2-1}): Hickory (HI) only")
    print(f"  Lower half (rows {N//2}-{N-1}): Red Oak (RO) only")
    print(f"\nTransition rules:")
    print(f"  If current cell is RO:")
    print(f"    - All 8 neighbors are RO → stay RO (probability 1.0)")
    print(f"    - Otherwise → RO: {transition_probabilities[0][0]:.2f}, HI: {transition_probabilities[0][1]:.2f}")
    print(f"  If current cell is HI:")
    print(f"    - All 8 neighbors are HI → stay HI (probability 1.0)")
    print(f"    - Otherwise → RO: {transition_probabilities[1][0]:.2f}, HI: {transition_probabilities[1][1]:.2f}")
    print("="*70 + "\n")
    
    # Create initial lattice - Two-plantation setup
    print("Creating initial lattice (two-plantation setup)...")
    initial_lattice = create_half_split_lattice(N)
    
    # Alternative: Use random initialization instead
    # Uncomment the line below to use random initial condition:
    # initial_lattice = create_random_lattice(N, p_RO=0.5, seed=SEED)
    
    # ===================================================================
    # SIMULATION
    # ===================================================================
    
    print("Running simulation with Moore neighborhood dynamics...")
    history, counts_history = run_simulation(
        initial_lattice, 
        T, 
        transition_probabilities, 
        seed=SEED
    )
    print(f"Simulation complete! ({T} time steps)\n")
    
    # ===================================================================
    # VISUALIZATION AND OUTPUT
    # ===================================================================
    
    # Print statistics
    print_statistics(counts_history)
    
    # Plot initial state
    print("Plotting initial state...")
    plot_lattice(
        history[0], 
        title=f"Initial Forest State (t=0)\nUpper: HI (green), Lower: RO (red)",
        filename="initial_state.png",
        show=show_plots
    )
    
    # Plot final state
    print("Plotting final state...")
    plot_lattice(
        history[-1], 
        title=f"Final Forest State (t={T})\nMoore Neighborhood Model",
        filename="final_state.png",
        show=show_plots
    )
    
    # Plot time series
    print("Plotting time series...")
    plot_time_series(
        counts_history,
        filename="time_series.png",
        show=show_plots
    )
    
    # Create animation (optional)
    if save_animation:
        print("Creating animation (this may take a moment)...")
        create_animation(
            history, 
            filename="forest_animation.gif",
            interval=animation_interval
        )
    
    print("\n" + "="*70)
    print("SIMULATION COMPLETE!")
    print("="*70)
    print("Generated files:")
    print("  - initial_state.png      (Initial two-plantation configuration)")
    print("  - final_state.png        (Final lattice state)")
    print("  - time_series.png        (Population dynamics over time)")
    if save_animation:
        print("  - forest_animation.gif   (Animated lattice evolution)")
    print("="*70 + "\n")
    
    # ===================================================================
    # ADDITIONAL ANALYSIS (OPTIONAL)
    # ===================================================================
    
    # You can add additional analysis here, for example:
    # - Calculate interface width between species
    # - Measure spatial correlation
    # - Compute domain sizes
    # - Analyze invasion dynamics
    
    # Example: Print some intermediate states
    print("Sample time points:")
    milestones = [0, T//4, T//2, 3*T//4, T]
    for t in milestones:
        ro_count = counts_history[t, 0]
        hi_count = counts_history[t, 1]
        total = ro_count + hi_count
        print(f"  t={t:4d}: RO={ro_count:5d} ({100*ro_count/total:5.2f}%), "
              f"HI={hi_count:5d} ({100*hi_count/total:5.2f}%)")
    print()


if __name__ == "__main__":
    main()