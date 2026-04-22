"""
forest.py

Main entry point for the stochastic forest model simulation.

This script configures and runs the forest simulation with the following features:
- Modular design for easy extension
- Configurable parameters
- Visualization of results
- Statistical output
"""

import numpy as np
from P01_initialization import create_random_lattice
from P01_dynamics import run_simulation
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
    N = 50
    
    # Number of time steps
    T = 100
    
    # Random seed for reproducibility (set to None for random results)
    SEED = 42
    
    # Initial distribution (probability of Red Oak)
    initial_p_RO = 0.5
    
    # Transition probabilities
    # Format: {state: [P(->RO), P(->HI)]}
    # State 0 = Red Oak (RO), State 1 = Hickory (HI)
    transition_probabilities = {
        0: [0.50, 0.50],  # RO -> RO with 50%, RO -> HI with 50%
        1: [0.74, 0.26]   # HI -> RO with 74%, HI -> HI with 26%
    }
    
    # Visualization options
    save_animation = True  # Set to False to skip animation (saves time)
    show_plots = True      # Set to False to only save plots without displaying
    
    # ===================================================================
    # INITIALIZATION
    # ===================================================================
    
    print("="*60)
    print("STOCHASTIC FOREST MODEL SIMULATION")
    print("="*60)
    print(f"Lattice size: {N} x {N}")
    print(f"Time steps: {T}")
    print(f"Random seed: {SEED}")
    print(f"Initial P(RO): {initial_p_RO}")
    print(f"Transition rules:")
    print(f"  RO -> RO: {transition_probabilities[0][0]:.2f}")
    print(f"  RO -> HI: {transition_probabilities[0][1]:.2f}")
    print(f"  HI -> RO: {transition_probabilities[1][0]:.2f}")
    print(f"  HI -> HI: {transition_probabilities[1][1]:.2f}")
    print("="*60 + "\n")
    
    # Create initial lattice
    print("Creating initial lattice...")
    initial_lattice = create_random_lattice(N, p_RO=initial_p_RO, seed=SEED)
    
    # ===================================================================
    # SIMULATION
    # ===================================================================
    
    print("Running simulation...")
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
        title=f"Initial Forest State (t=0)",
        filename="initial_state.png",
        show=show_plots
    )
    
    # Plot final state
    print("Plotting final state...")
    plot_lattice(
        history[-1], 
        title=f"Final Forest State (t={T})",
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
        print("Creating animation...")
        create_animation(
            history, 
            filename="forest_animation.gif",
            interval=100  # 100ms between frames
        )
    
    print("\n" + "="*60)
    print("SIMULATION COMPLETE!")
    print("="*60)
    print("Generated files:")
    print("  - initial_state.png")
    print("  - final_state.png")
    print("  - time_series.png")
    if save_animation:
        print("  - forest_animation.gif")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()