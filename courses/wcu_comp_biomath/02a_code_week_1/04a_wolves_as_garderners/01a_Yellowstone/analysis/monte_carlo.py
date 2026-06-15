"""
Monte Carlo analysis for wolf density effects.
"""

import numpy as np
from model.simulation import Simulation
from config.config import N_STEPS, NX, NY, N_BISON
import os
import time


def run_monte_carlo_wolf_density(wolf_counts=None, n_runs=50, n_steps=None, verbose=True):
    """
    Run Monte Carlo simulation varying wolf density.
    
    Args:
        wolf_counts: List of wolf numbers to test (default: [0, 5, 10, 15, 20, 30])
        n_runs: Number of replicate runs per wolf count
        n_steps: Number of simulation steps (uses config.N_STEPS if None)
        verbose: Print progress information
        
    Returns:
        dict: Results with mean and std for each wolf count
    """
    if wolf_counts is None:
        wolf_counts = [0, 5, 10, 15, 20, 30]
    
    if n_steps is None:
        n_steps = N_STEPS
    
    results = {}
    
    if verbose:
        print("=" * 70)
        print("MONTE CARLO ANALYSIS: WOLF DENSITY EFFECTS")
        print("=" * 70)
        print(f"Runs per wolf count: {n_runs}")
        print(f"Steps per run: {n_steps}")
        print(f"Grid size: {NX} x {NY}")
        print(f"Bison: {N_BISON}")
        print(f"Wolf counts to test: {wolf_counts}")
        print(f"Total simulations: {len(wolf_counts) * n_runs}")
        print("=" * 70)
    
    total_sims = len(wolf_counts) * n_runs
    sim_counter = 0
    start_time = time.time()
    
    for n_wolves in wolf_counts:
        if verbose:
            print(f"\n{'='*70}")
            print(f"Testing {n_wolves} wolves ({n_runs} runs):")
            print(f"{'='*70}")
        
        forest_final = []
        encounters_total = []
        
        for run in range(n_runs):
            sim_counter += 1
            
            # Use different random seed for each run
            seed = 1000 * n_wolves + run
            
            if verbose:
                elapsed = time.time() - start_time
                avg_time = elapsed / sim_counter if sim_counter > 0 else 0
                remaining = (total_sims - sim_counter) * avg_time
                print(f"  Run {run+1}/{n_runs} (Overall: {sim_counter}/{total_sims}, "
                      f"ETA: {remaining:.0f}s)...", end='', flush=True)
            
            try:
                sim = Simulation(
                    n_wolves=n_wolves,
                    random_seed=seed
                )
                
                sim.run(n_steps=n_steps, verbose=False)
                
                # Extract final forest count
                forest_final.append(sim.statistics['forest_cells'][-1])
                
                # Extract total encounters
                encounters_total.append(sum(sim.statistics['wolf_bison_encounters']))
                
                if verbose:
                    print(f" ✓ Forest={forest_final[-1]}, Encounters={encounters_total[-1]}")
                
            except Exception as e:
                print(f" ERROR: {e}")
                # Add NaN for failed runs
                forest_final.append(np.nan)
                encounters_total.append(np.nan)
        
        # Calculate statistics (ignore NaN values)
        results[n_wolves] = {
            'forest_mean': np.nanmean(forest_final),
            'forest_std': np.nanstd(forest_final, ddof=1),
            'encounters_mean': np.nanmean(encounters_total),
            'encounters_std': np.nanstd(encounters_total, ddof=1),
            'forest_raw': forest_final,
            'encounters_raw': encounters_total,
            'n_successful': np.sum(~np.isnan(forest_final))
        }
        
        if verbose:
            print(f"\n  Summary for {n_wolves} wolves:")
            print(f"    Forest: {results[n_wolves]['forest_mean']:.1f} ± {results[n_wolves]['forest_std']:.1f}")
            print(f"    Encounters: {results[n_wolves]['encounters_mean']:.1f} ± {results[n_wolves]['encounters_std']:.1f}")
            print(f"    Successful runs: {results[n_wolves]['n_successful']}/{n_runs}")
    
    if verbose:
        total_time = time.time() - start_time
        print(f"\n{'='*70}")
        print(f"Total time: {total_time:.1f}s ({total_time/total_sims:.2f}s per simulation)")
        print(f"{'='*70}")
    
    return results


def print_monte_carlo_results(results):
    """
    Print formatted Monte Carlo results.
    
    Args:
        results: Dictionary from run_monte_carlo_wolf_density()
    """
    print("\n" + "=" * 70)
    print("MONTE CARLO RESULTS")
    print("=" * 70)
    print(f"{'Wolves':<10} {'Forest (mean ± std)':<30} {'Encounters (mean ± std)':<30}")
    print("-" * 70)
    
    for n_wolves in sorted(results.keys()):
        r = results[n_wolves]
        forest_str = f"{r['forest_mean']:.1f} ± {r['forest_std']:.1f}"
        encounters_str = f"{r['encounters_mean']:.1f} ± {r['encounters_std']:.1f}"
        print(f"{n_wolves:<10} {forest_str:<30} {encounters_str:<30}")
    
    print("=" * 70)


def save_monte_carlo_results(results, filename='monte_carlo_results.txt'):
    """
    Save Monte Carlo results to file.
    
    Args:
        results: Dictionary from run_monte_carlo_wolf_density()
        filename: Output filename
    """
    from config.config import OUTPUT_DIR
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("MONTE CARLO RESULTS: WOLF DENSITY EFFECTS\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"{'Wolves':<10} {'Forest (mean ± std)':<30} {'Encounters (mean ± std)':<30}\n")
        f.write("-" * 70 + "\n")
        
        for n_wolves in sorted(results.keys()):
            r = results[n_wolves]
            forest_str = f"{r['forest_mean']:.1f} ± {r['forest_std']:.1f}"
            encounters_str = f"{r['encounters_mean']:.1f} ± {r['encounters_std']:.1f}"
            f.write(f"{n_wolves:<10} {forest_str:<30} {encounters_str:<30}\n")
        
        f.write("=" * 70 + "\n")
    
    print(f"\nResults saved to: {filepath}")


# TEST FUNCTION
def test_monte_carlo():
    """
    Quick test with small parameters.
    """
    print("\n" + "=" * 70)
    print("QUICK TEST - Monte Carlo")
    print("=" * 70)
    
    results = run_monte_carlo_wolf_density(
        wolf_counts=[0, 10],  # Only 2 wolf counts
        n_runs=3,             # Only 3 runs each
        n_steps=50,           # Only 50 steps per run
        verbose=True
    )
    
    print_monte_carlo_results(results)
    
    print("\n✓ Test completed successfully!")
    return results


if __name__ == "__main__":
    # Run quick test first
    print("Running quick test...")
    test_results = test_monte_carlo()
    
    print("\n" + "=" * 70)
    proceed = input("Test successful. Run full analysis? (y/n): ").strip().lower()
    
    if proceed == 'y':
        # Run full Monte Carlo analysis
        results = run_monte_carlo_wolf_density(
            wolf_counts=[0, 5, 10, 15, 20, 30],
            n_runs=50,
            n_steps=500,
            verbose=True
        )
        
        print_monte_carlo_results(results)
        save_monte_carlo_results(results)