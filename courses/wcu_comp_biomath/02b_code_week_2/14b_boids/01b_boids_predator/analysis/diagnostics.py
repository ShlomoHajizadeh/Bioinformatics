"""
Diagnostic tools for analyzing simulation results.
"""
import numpy as np
import matplotlib.pyplot as plt
from analysis.metrics import compute_metrics, compute_time_series_metrics


def run_diagnostics(history, config):
    """
    Run comprehensive diagnostics on simulation results.
    
    Args:
        history: list of State objects
        config: Configuration object
    """
    print("\nSimulation parameters:")
    print(f"  Domain: {config.domain_size}")
    print(f"  Total agents: {config.n_agents}")
    
    if hasattr(config, 'n_species1'):
        print(f"  Species 1: {config.n_species1}")
        print(f"  Species 2: {config.n_species2}")
    
    print(f"  Time steps: {config.n_steps}")
    print(f"  dt: {config.dt}")
    
    # Compute time series metrics
    time_series = compute_time_series_metrics(history, config)
    
    # Final state metrics
    final_metrics = compute_metrics(history[-1], config)
    
    print("\nFinal state metrics:")
    print(f"  Mean speed: {final_metrics['mean_speed']:.3f}")
    print(f"  Polarization: {final_metrics['polarization']:.3f}")
    print(f"  Mean neighbors: {final_metrics['mean_neighbors']:.1f}")
    
    # Species-specific metrics
    if hasattr(config, 'species1_label'):
        for species_label in [config.species1_label, config.species2_label]:
            prefix = f'species_{species_label}_'
            if prefix + 'mean_speed' in final_metrics:
                print(f"\nSpecies {species_label}:")
                print(f"  Count: {final_metrics[prefix + 'count']}")
                print(f"  Mean speed: {final_metrics[prefix + 'mean_speed']:.3f}")
                print(f"  Polarization: {final_metrics[prefix + 'polarization']:.3f}")
    
    # Time evolution statistics
    print("\nTime evolution:")
    print(f"  Speed range: [{np.min(time_series['mean_speed']):.3f}, {np.max(time_series['mean_speed']):.3f}]")
    print(f"  Polarization range: [{np.min(time_series['polarization']):.3f}, {np.max(time_series['polarization']):.3f}]")
    
    # Create diagnostic plots
    plot_diagnostics(time_series, config)


def plot_diagnostics(time_series, config):
    """
    Create diagnostic plots.
    
    Args:
        time_series: dictionary of time series data
        config: Configuration object
    """
    # Check which species data is available
    has_species1 = f'species_{config.species1_label}_mean_speed' in time_series if hasattr(config, 'species1_label') else False
    has_species2 = f'species_{config.species2_label}_mean_speed' in time_series if hasattr(config, 'species2_label') else False
    has_species = has_species1 and has_species2
    
    # Determine number of subplots
    n_plots = 5 if has_species else 4
    
    fig, axes = plt.subplots(n_plots, 1, figsize=(10, 3*n_plots))
    
    # Plot 1: Mean speed over time
    axes[0].plot(time_series['time'], time_series['mean_speed'], 'b-', linewidth=2)
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Mean Speed')
    axes[0].set_title('Mean Speed Evolution')
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Polarization over time
    axes[1].plot(time_series['time'], time_series['polarization'], 'g-', linewidth=2)
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Polarization')
    axes[1].set_title('Polarization Evolution (1 = perfectly aligned)')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim([0, 1.1])
    
    # Plot 3: Angular momentum over time
    axes[2].plot(time_series['time'], time_series['angular_momentum'], 'r-', linewidth=2)
    axes[2].set_xlabel('Time')
    axes[2].set_ylabel('Angular Momentum')
    axes[2].set_title('Angular Momentum Evolution')
    axes[2].grid(True, alpha=0.3)
    
    # Plot 4: Mean neighbors over time
    axes[3].plot(time_series['time'], time_series['mean_neighbors'], 'm-', linewidth=2)
    axes[3].set_xlabel('Time')
    axes[3].set_ylabel('Mean Neighbors')
    axes[3].set_title('Mean Number of Neighbors')
    axes[3].grid(True, alpha=0.3)
    
    # Plot 5: Species-specific speeds (if available)
    if has_species:
        species1_key = f'species_{config.species1_label}_mean_speed'
        species2_key = f'species_{config.species2_label}_mean_speed'
        
        axes[4].plot(time_series['time'], time_series[species1_key], 
                    'b-', linewidth=2, label=f'Species {config.species1_label} (Prey)')
        axes[4].plot(time_series['time'], time_series[species2_key], 
                    'r-', linewidth=2, label=f'Species {config.species2_label} (Predators)')
        axes[4].set_xlabel('Time')
        axes[4].set_ylabel('Mean Speed')
        axes[4].set_title('Species-Specific Speed Evolution')
        axes[4].legend()
        axes[4].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    filename = 'diagnostics_2d.png' if config.dimension == 2 else 'diagnostics_3d.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nDiagnostic plots saved to {filename}")
    plt.close()


def compute_statistics_summary(history, config):
    """
    Compute summary statistics for the entire simulation.
    
    Args:
        history: list of State objects
        config: Configuration object
        
    Returns:
        dict: summary statistics
    """
    time_series = compute_time_series_metrics(history, config)
    
    summary = {
        'mean_speed_avg': np.mean(time_series['mean_speed']),
        'mean_speed_std': np.std(time_series['mean_speed']),
        'polarization_avg': np.mean(time_series['polarization']),
        'polarization_std': np.std(time_series['polarization']),
        'angular_momentum_avg': np.mean(time_series['angular_momentum']),
        'angular_momentum_std': np.std(time_series['angular_momentum']),
        'mean_neighbors_avg': np.mean(time_series['mean_neighbors']),
        'mean_neighbors_std': np.std(time_series['mean_neighbors']),
    }
    
    return summary


def print_statistics_summary(history, config):
    """
    Print summary statistics.
    
    Args:
        history: list of State objects
        config: Configuration object
    """
    summary = compute_statistics_summary(history, config)
    
    print("\n" + "="*60)
    print("SIMULATION SUMMARY STATISTICS")
    print("="*60)
    
    print(f"\nMean Speed:")
    print(f"  Average: {summary['mean_speed_avg']:.3f} ± {summary['mean_speed_std']:.3f}")
    
    print(f"\nPolarization:")
    print(f"  Average: {summary['polarization_avg']:.3f} ± {summary['polarization_std']:.3f}")
    
    print(f"\nAngular Momentum:")
    print(f"  Average: {summary['angular_momentum_avg']:.3f} ± {summary['angular_momentum_std']:.3f}")
    
    print(f"\nMean Neighbors:")
    print(f"  Average: {summary['mean_neighbors_avg']:.1f} ± {summary['mean_neighbors_std']:.1f}")
    
    print("="*60 + "\n")


def analyze_species_separation(history, config):
    """
    Analyze separation between species over time.
    
    Args:
        history: list of State objects
        config: Configuration object
        
    Returns:
        dict: separation metrics
    """
    if not hasattr(config, 'species1_label'):
        return None
    
    n_snapshots = len(history)
    separations = np.zeros(n_snapshots)
    
    for i, state in enumerate(history):
        mask1 = state.species == config.species1_label
        mask2 = state.species == config.species2_label
        
        if np.any(mask1) and np.any(mask2):
            com1 = np.mean(state.positions[mask1], axis=0)
            com2 = np.mean(state.positions[mask2], axis=0)
            separations[i] = np.linalg.norm(com2 - com1)
    
    return {
        'time': np.arange(n_snapshots) * config.dt * config.save_every,
        'separation': separations,
        'mean_separation': np.mean(separations),
        'std_separation': np.std(separations),
    }


def plot_species_separation(history, config):
    """
    Plot separation between species over time.
    
    Args:
        history: list of State objects
        config: Configuration object
    """
    sep_data = analyze_species_separation(history, config)
    
    if sep_data is None:
        return
    
    plt.figure(figsize=(10, 4))
    plt.plot(sep_data['time'], sep_data['separation'], 'b-', linewidth=2)
    plt.xlabel('Time')
    plt.ylabel('Center-of-Mass Separation')
    plt.title('Distance Between Prey and Predator Centers of Mass')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = 'species_separation.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Species separation plot saved to {filename}")
    plt.close()


def export_metrics_csv(history, config, filename='metrics.csv'):
    """
    Export time series metrics to CSV file.
    
    Args:
        history: list of State objects
        config: Configuration object
        filename: output filename
    """
    time_series = compute_time_series_metrics(history, config)
    
    # Create header
    header = ','.join(time_series.keys())
    
    # Stack data
    data = np.column_stack([time_series[key] for key in time_series.keys()])
    
    # Save to CSV
    np.savetxt(filename, data, delimiter=',', header=header, comments='')
    print(f"Metrics exported to {filename}")