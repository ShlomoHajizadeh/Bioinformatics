"""
Metrics for analyzing boids simulation results.
"""
import numpy as np


def compute_metrics(state, config):
    """
    Compute various metrics for a simulation state.
    
    Args:
        state: State object
        config: Configuration object
        
    Returns:
        dict: Dictionary of computed metrics
    """
    metrics = {}
    
    # Average speed
    speeds = np.linalg.norm(state.velocities, axis=1)
    metrics['avg_speed'] = np.mean(speeds)
    metrics['std_speed'] = np.std(speeds)
    
    # Polarization (order parameter)
    # Measures alignment of velocities
    avg_velocity = np.mean(state.velocities, axis=0)
    metrics['polarization'] = np.linalg.norm(avg_velocity) / (metrics['avg_speed'] + 1e-10)
    
    # Species-specific metrics
    for species_label in [config.species1_label, config.species2_label]:
        mask = state.get_species_mask(species_label)
        species_name = f"sp{species_label + 1}"
        
        if np.any(mask):
            species_velocities = state.velocities[mask]
            species_speeds = speeds[mask]
            
            metrics[f'avg_speed_{species_name}'] = np.mean(species_speeds)
            metrics[f'std_speed_{species_name}'] = np.std(species_speeds)
            
            # Polarization for this species
            avg_vel_species = np.mean(species_velocities, axis=0)
            metrics[f'polarization_{species_name}'] = (
                np.linalg.norm(avg_vel_species) / (metrics[f'avg_speed_{species_name}'] + 1e-10)
            )
    
    # Neighbor counts (requires computing neighbors)
    from core.neighbors import find_neighbors
    from core.domain import Domain
    
    domain = Domain(config.domain_size)
    
    # For species 1
    params_sp1 = config.get_species_params(config.species1_label)
    r_max_sp1 = max(params_sp1['r_avoidance'], params_sp1['r_alignment'], params_sp1['r_cohesion'])
    neighbors_sp1 = find_neighbors(state, domain, r_max_sp1, config.species1_label)
    
    neighbor_counts_sp1 = [len(neighs) for neighs in neighbors_sp1]
    metrics['mean_neighbors_sp1'] = np.mean(neighbor_counts_sp1) if neighbor_counts_sp1 else 0
    metrics['std_neighbors_sp1'] = np.std(neighbor_counts_sp1) if neighbor_counts_sp1 else 0
    
    # For species 2
    params_sp2 = config.get_species_params(config.species2_label)
    r_max_sp2 = params_sp2['r_avoidance']
    neighbors_sp2 = find_neighbors(state, domain, r_max_sp2, config.species2_label)
    
    neighbor_counts_sp2 = [len(neighs) for neighs in neighbors_sp2]
    metrics['mean_neighbors_sp2'] = np.mean(neighbor_counts_sp2) if neighbor_counts_sp2 else 0
    metrics['std_neighbors_sp2'] = np.std(neighbor_counts_sp2) if neighbor_counts_sp2 else 0
    
    # Spatial extent (how spread out are the agents)
    center_of_mass = np.mean(state.positions, axis=0)
    distances_from_com = np.linalg.norm(state.positions - center_of_mass, axis=1)
    metrics['spatial_extent'] = np.mean(distances_from_com)
    metrics['max_extent'] = np.max(distances_from_com)
    
    return metrics


def compute_time_series_metrics(history, config):
    """
    Compute metrics over time from simulation history.
    
    Args:
        history: list of State objects
        config: Configuration object
        
    Returns:
        dict: Dictionary with time series of metrics
    """
    time_series = {
        'time': [],
        'avg_speed': [],
        'polarization': [],
        'mean_neighbors_sp1': [],
        'mean_neighbors_sp2': [],
        'spatial_extent': []
    }
    
    for t, state in enumerate(history):
        metrics = compute_metrics(state, config)
        
        time_series['time'].append(t * config.dt * config.save_every)
        time_series['avg_speed'].append(metrics['avg_speed'])
        time_series['polarization'].append(metrics['polarization'])
        time_series['mean_neighbors_sp1'].append(metrics['mean_neighbors_sp1'])
        time_series['mean_neighbors_sp2'].append(metrics['mean_neighbors_sp2'])
        time_series['spatial_extent'].append(metrics['spatial_extent'])
    
    # Convert to numpy arrays
    for key in time_series:
        time_series[key] = np.array(time_series[key])
    
    return time_series