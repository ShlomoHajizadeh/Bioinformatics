"""
Main entry point for Yellowstone simulation.
"""

import os
from model.simulation import Simulation
from visualization.plot import plot_combined_state, plot_time_series
from visualization.animation import create_animation
from config.config import OUTPUT_DIR, SAVE_PLOTS, N_STEPS, RANDOM_SEED


def run_basic_simulation():
    """
    Run basic simulation with default parameters.
    """
    print("=" * 70)
    print("YELLOWSTONE WOLF-BISON ECOSYSTEM SIMULATION")
    print("=" * 70)
    
    # Initialize simulation (no wolf_move_period parameter!)
    sim = Simulation(
        random_seed=RANDOM_SEED
    )
    
    # Run simulation
    print("\nRunning simulation...")
    sim.run(n_steps=N_STEPS, verbose=True)
    
    # Create visualizations
    if SAVE_PLOTS:
        print("\n" + "=" * 70)
        print("CREATING VISUALIZATIONS")
        print("=" * 70)
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Plot final state
        print("\nCreating final state plot...")
        plot_combined_state(sim, filename='final_state.png')
        
        # Plot time series
        print("Creating time series plot...")
        plot_time_series(sim, filename='time_series.png')
        
        print(f"\nAll outputs saved to '{OUTPUT_DIR}/' directory")
    
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)


def run_custom_simulation():
    """
    Run simulation with custom parameters.
    """
    print("\n" + "=" * 70)
    print("CUSTOM SIMULATION")
    print("=" * 70)
    
    # Get custom parameters
    try:
        nx = int(input("Grid width (default 50): ") or 50)
        ny = int(input("Grid height (default 50): ") or 50)
        n_bison = int(input("Number of bison (default 300): ") or 300)
        n_wolves = int(input("Number of wolves (default 15): ") or 15)
        n_steps = int(input("Number of steps (default 500): ") or 500)
        seed = input("Random seed (default 42, press Enter for default): ")
        seed = int(seed) if seed else 42
    except ValueError:
        print("Invalid input. Using default values.")
        nx, ny, n_bison, n_wolves, n_steps, seed = 50, 50, 300, 15, 500, 42
    
    # Initialize and run
    sim = Simulation(
        nx=nx,
        ny=ny,
        n_bison=n_bison,
        n_wolves=n_wolves,
        random_seed=seed
    )
    
    sim.run(n_steps=n_steps, verbose=True)
    
    # Create visualizations
    if SAVE_PLOTS:
        print("\nCreating visualizations...")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        plot_combined_state(sim, filename='custom_final_state.png')
        plot_time_series(sim, filename='custom_time_series.png')
        
        print(f"Outputs saved to '{OUTPUT_DIR}/' directory")
    
    print("\nSimulation complete!")


def run_comparison():
    """
    Run multiple simulations with different wolf densities.
    """
    print("\n" + "=" * 70)
    print("WOLF DENSITY COMPARISON")
    print("=" * 70)
    
    wolf_counts = [0, 5, 10, 15, 20, 30]
    results = {}
    
    for n_wolves in wolf_counts:
        print(f"\nRunning simulation with {n_wolves} wolves...")
        
        sim = Simulation(
            n_wolves=n_wolves,
            random_seed=RANDOM_SEED
        )
        
        sim.run(n_steps=N_STEPS, verbose=False)
        
        # Store final statistics
        results[n_wolves] = {
            'forest_cells': sim.statistics['forest_cells'][-1],
            'mean_grass_stage': sim.statistics['mean_grass_stage'][-1],
            'overgrazed_cells': sim.statistics['overgrazed_cells'][-1],
            'total_encounters': sum(sim.statistics['wolf_bison_encounters'])
        }
    
    # Print comparison
    print("\n" + "=" * 70)
    print("COMPARISON RESULTS")
    print("=" * 70)
    print(f"{'Wolves':<10} {'Forest':<10} {'Grass Stage':<15} {'Overgrazed':<12} {'Encounters':<12}")
    print("-" * 70)
    
    for n_wolves in wolf_counts:
        r = results[n_wolves]
        print(f"{n_wolves:<10} {r['forest_cells']:<10} {r['mean_grass_stage']:<15.2f} "
              f"{r['overgrazed_cells']:<12} {r['total_encounters']:<12}")
    
    print("\nComparison complete!")


def create_animation_only():
    """
    Run simulation and create animation.
    """
    print("\n" + "=" * 70)
    print("CREATING ANIMATION")
    print("=" * 70)
    
    print("\nRunning simulation with state history...")
    sim = Simulation(random_seed=RANDOM_SEED)
    
    # Run with state history enabled, save every 5 steps
    sim.run(n_steps=N_STEPS, verbose=True, save_history=True, history_interval=5)
    
    print("\nCreating animation (this may take a while)...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    create_animation(sim, filename='simulation.gif', fps=10)
    
    print(f"\n✓ Complete!")


def show_statistics():
    """
    Run simulation and show detailed statistics.
    """
    print("\n" + "=" * 70)
    print("DETAILED STATISTICS")
    print("=" * 70)
    
    sim = Simulation(random_seed=RANDOM_SEED)
    sim.run(n_steps=N_STEPS, verbose=True)
    
    stats = sim.statistics
    
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    
    print(f"\nInitial state:")
    print(f"  Forest cells: {stats['forest_cells'][0]}")
    print(f"  Mean grass stage: {stats['mean_grass_stage'][0]:.2f}")
    print(f"  Overgrazed cells: {stats['overgrazed_cells'][0]}")
    
    print(f"\nFinal state (step {stats['step'][-1]}):")
    print(f"  Forest cells: {stats['forest_cells'][-1]}")
    print(f"  Mean grass stage: {stats['mean_grass_stage'][-1]:.2f}")
    print(f"  Overgrazed cells: {stats['overgrazed_cells'][-1]}")
    
    print(f"\nChanges:")
    print(f"  Forest gain: {stats['forest_cells'][-1] - stats['forest_cells'][0]}")
    print(f"  Grass stage change: {stats['mean_grass_stage'][-1] - stats['mean_grass_stage'][0]:.2f}")
    
    print(f"\nTotal events:")
    print(f"  Wolf-bison encounters: {sum(stats['wolf_bison_encounters'])}")
    print(f"  Bison escaped from wolves: {sum(stats['bison_escaped'])}")
    print(f"  Bison grazing moves: {sum(stats['bison_grazed'])}")
    print(f"  Bison social resolutions: {sum(stats['bison_resolved'])}")
    print(f"  Forest conversions: {sum(stats['forest_conversions'])}")

def run_monte_carlo():
    """
    Run Monte Carlo analysis of wolf density effects.
    """
    from analysis.monte_carlo import (
        run_monte_carlo_wolf_density,
        print_monte_carlo_results,
        save_monte_carlo_results
    )
    
    print("\n" + "=" * 70)
    print("MONTE CARLO ANALYSIS")
    print("=" * 70)
    
    # Get parameters
    try:
        n_runs = int(input("Number of runs per wolf count (default 50): ") or 50)
        n_steps = int(input("Steps per run (default 500): ") or 500)
    except ValueError:
        print("Invalid input. Using defaults: 50 runs, 500 steps")
        n_runs = 50
        n_steps = 500
    
    # Run analysis
    results = run_monte_carlo_wolf_density(
        wolf_counts=[0, 5, 10, 15, 20, 30],
        n_runs=n_runs,
        n_steps=n_steps,
        verbose=True
    )
    
    # Print and save results
    print_monte_carlo_results(results)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_monte_carlo_results(results)
    

def interactive_menu():
    """
    Display interactive menu for simulation options.
    """
    while True:
        print("\n" + "=" * 70)
        print("YELLOWSTONE SIMULATION - MENU")
        print("=" * 70)
        print("1. Run basic simulation")
        print("2. Run custom simulation")
        print("3. Compare wolf densities")
        print("4. Create animation")
        print("5. Show detailed statistics")
        print("6. Run Monte Carlo analysis")  # NEU
        print("7. Run all analyses")
        print("0. Exit")
        print("=" * 70)
        
        try:
            choice = input("\nSelect option (0-7): ").strip()
            
            if choice == '0':
                print("\nExiting. Goodbye!")
                break
            elif choice == '1':
                run_basic_simulation()
            elif choice == '2':
                run_custom_simulation()
            elif choice == '3':
                run_comparison()
            elif choice == '4':
                create_animation_only()
            elif choice == '5':
                show_statistics()
            elif choice == '6':
                run_monte_carlo()  # NEU
            elif choice == '7':
                run_basic_simulation()
                run_comparison()
                show_statistics()
                run_monte_carlo()  # NEU
            else:
                print("\nInvalid option. Please select 0-7.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


def main():
    """
    Main entry point.
    """
    # Create output directory
    if SAVE_PLOTS:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Run interactive menu
    interactive_menu()


if __name__ == "__main__":
    main()