"""
Diagnostic tools for Reynolds boids simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
from .metrics import compute_time_series_metrics


def run_diagnostics(history, config, save_plots=True):
    """
    Run comprehensive diagnostics on simulation results.
    
    Args:
        history: list of State objects
        config: Configuration object
        save_plots: whether to save diagnostic plots
    """
    print("\n" + "="*60)
    print("SIMULATION DIAGNOSTICS")
    print("="*60)
    
    # Compute time series
    time_series = compute_time_series_metrics(history, config)
    
    # Print summary statistics
    print(f"\nSimulation parameters:")
    print(f"  Domain: {config.domain_size}")
    print(f"  Total agents: {config.n_agents}")
    print(f"  Species 1: {config.n_species1}")
    print(f"  Species 2: {config.n_species2}")
    print(f"  Time steps: {config.n_steps}")
    print(f"  dt: {config.dt}")
    
    print(f"\nFinal state metrics:")
    print(f"  Average speed: {time_series['avg_speed'][-1]:.3f}")
    print(f"  Polarization: {time_series['polarization'][-1]:.3f}")
    print(f"  Mean neighbors (sp1): {time_series['mean_neighbors_sp1'][-1]:.2f}")
    print(f"  Mean neighbors (sp2): {time_series['mean_neighbors_sp2'][-1]:.2f}")
    print(f"  Spatial extent: {time_series['spatial_extent'][-1]:.2f}")
    
    # Check for equilibration
    print(f"\nEquilibration analysis:")
    
    # Use last 20% of simulation for equilibrium
    eq_start = int(0.8 * len(time_series['time']))
    
    polarization_eq = time_series['polarization'][eq_start:]
    pol_mean = np.mean(polarization_eq)
    pol_std = np.std(polarization_eq)
    
    print(f"  Polarization (last 20%): {pol_mean:.3f} ± {pol_std:.3f}")
    
    speed_eq = time_series['avg_speed'][eq_start:]
    speed_mean = np.mean(speed_eq)
    speed_std = np.std(speed_eq)
    
    print(f"  Avg speed (last 20%): {speed_mean:.3f} ± {speed_std:.3f}")
    
    # Detect potential issues
    print(f"\nPotential issues:")
    issues_found = False
    
    if pol_std / (pol_mean + 1e-10) > 0.2:
        print("  ⚠ High polarization fluctuations - system may not be equilibrated")
        issues_found = True
    
    if time_series['avg_speed'][-1] < 0.1:
        print("  ⚠ Very low speeds - agents may be stuck")
        issues_found = True
    
    if time_series['mean_neighbors_sp1'][-1] < 1.0:
        print("  ⚠ Low neighbor count - agents may be too sparse")
        issues_found = True
    
    if not issues_found:
        print("  ✓ No obvious issues detected")
    
    # Create diagnostic plots
    if save_plots:
        create_diagnostic_plots(time_series, config)
        print(f"\nDiagnostic plots saved to 'diagnostics.png'")
    
    print("="*60 + "\n")


def create_diagnostic_plots(time_series, config):
    """
    Create diagnostic plots for simulation analysis.
    
    Args:
        time_series: dict of time series data
        config: Configuration object
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Average speed over time
    ax = axes[0, 0]
    ax.plot(time_series['time'], time_series['avg_speed'], 'b-', linewidth=1.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Average Speed')
    ax.set_title('Average Speed Over Time')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Polarization over time
    ax = axes[0, 1]
    ax.plot(time_series['time'], time_series['polarization'], 'r-', linewidth=1.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Polarization')
    ax.set_title('Polarization (Order Parameter)')
    ax.set_ylim([0, 1.1])
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Neighbor counts over time
    ax = axes[1, 0]
    ax.plot(time_series['time'], time_series['mean_neighbors_sp1'], 
            'g-', linewidth=1.5, label='Species 1')
    ax.plot(time_series['time'], time_series['mean_neighbors_sp2'], 
            'orange', linewidth=1.5, label='Species 2')
    ax.set_xlabel('Time')
    ax.set_ylabel('Mean Neighbors')
    ax.set_title('Average Neighbor Count')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Spatial extent over time
    ax = axes[1, 1]
    ax.plot(time_series['time'], time_series['spatial_extent'], 
            'purple', linewidth=1.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Spatial Extent')
    ax.set_title('Spatial Extent (Spread)')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('diagnostics.png', dpi=150, bbox_inches='tight')
    plt.close()


def check_conservation_laws(history, config):
    """
    Check if any conservation laws hold (for verification).
    
    Args:
        history: list of State objects
        config: Configuration object
        
    Returns:
        dict: Conservation check results
    """
    results = {}
    
    # Total momentum (should be conserved in absence of external forces)
    momenta = []
    for state in history:
        total_momentum = np.sum(state.velocities, axis=0)
        momenta.append(total_momentum)
    
    momenta = np.array(momenta)
    momentum_variation = np.std(momenta, axis=0)
    
    results['momentum_conserved'] = np.all(momentum_variation < 0.1)
    results['momentum_variation'] = momentum_variation
    
    # Number of agents (should be exactly conserved)
    n_agents = [state.n_agents for state in history]
    results['n_agents_conserved'] = all(n == config.n_agents for n in n_agents)
    
    return results