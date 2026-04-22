"""
Metrics for analyzing boids simulations.
"""
import numpy as np
from core.domain import Domain


def compute_polarization(velocities):
    """
    Compute polarization (alignment) of velocities.
    
    Args:
        velocities: array of velocity vectors
        
    Returns:
        polarization value (0 to 1, where 1 is perfectly aligned)
    """
    if len(velocities) == 0:
        return 0.0
    
    # Normalize velocities
    speeds = np.linalg.norm(velocities, axis=1, keepdims=True)
    speeds = np.maximum(speeds, 1e-10)  # Avoid division by zero
    directions = velocities / speeds
    
    # Average direction
    avg_direction = np.mean(directions, axis=0)
    
    # Polarization is magnitude of average direction
    polarization = np.linalg.norm(avg_direction)
    
    return polarization


def compute_metrics(state, config):
    """
    Compute various metrics for the current state.
    
    Args:
        state: State object
        config: Configuration object
        
    Returns:
        dict of metrics
    """
    domain = Domain(config.domain_size)
    
    metrics = {}
    
    # Basic metrics
    speeds = np.linalg.norm(state.velocities, axis=1)
    metrics['mean_speed'] = np.mean(speeds)
    metrics['std_speed'] = np.std(speeds)
    metrics['polarization'] = compute_polarization(state.velocities)
    
    # Angular momentum (for detecting rotation)
    center = np.mean(state.positions, axis=0)
    relative_pos = state.positions - center
    
    if state.positions.shape[1] == 2:
        # 2D: angular momentum is scalar
        angular_momentum = np.sum(relative_pos[:, 0] * state.velocities[:, 1] - 
                                 relative_pos[:, 1] * state.velocities[:, 0])
    else:
        # 3D: angular momentum is vector
        angular_momentum = np.linalg.norm(np.cross(relative_pos, state.velocities).sum(axis=0))
    
    metrics['angular_momentum'] = angular_momentum
    
    # Neighbor statistics (using alignment radius as reference)
    if hasattr(config, 'r_align'):
        from core.neighbors import find_neighbors_efficient
        neighbors = find_neighbors_efficient(state.positions, domain, config.r_align)
        n_neighbors = [len(n) for n in neighbors]
        metrics['mean_neighbors'] = np.mean(n_neighbors)
        metrics['std_neighbors'] = np.std(n_neighbors)
    else:
        metrics['mean_neighbors'] = 0
        metrics['std_neighbors'] = 0
    
    # Species-specific metrics
    if hasattr(config, 'species1_label'):
        for species_label in [config.species1_label, config.species2_label]:
            mask = state.species == species_label
            if np.any(mask):
                species_velocities = state.velocities[mask]
                species_speeds = np.linalg.norm(species_velocities, axis=1)
                
                prefix = f'species_{species_label}_'
                metrics[prefix + 'count'] = np.sum(mask)
                metrics[prefix + 'mean_speed'] = np.mean(species_speeds)
                metrics[prefix + 'std_speed'] = np.std(species_speeds)
                metrics[prefix + 'polarization'] = compute_polarization(species_velocities)
    
    return metrics


def compute_center_of_mass(positions, species=None, species_label=None):
    """
    Compute center of mass.
    
    Args:
        positions: array of positions
        species: array of species labels (optional)
        species_label: specific species to compute COM for (optional)
        
    Returns:
        center of mass position
    """
    if species is not None and species_label is not None:
        mask = species == species_label
        if np.any(mask):
            return np.mean(positions[mask], axis=0)
        else:
            return None
    else:
        return np.mean(positions, axis=0)


def compute_spread(positions, center=None):
    """
    Compute spatial spread (standard deviation from center).
    
    Args:
        positions: array of positions
        center: center point (if None, use center of mass)
        
    Returns:
        spread value
    """
    if center is None:
        center = np.mean(positions, axis=0)
    
    distances = np.linalg.norm(positions - center, axis=1)
    return np.std(distances)


def compute_time_series_metrics(history, config):
    """
    Compute metrics for entire simulation history.
    
    Args:
        history: list of State objects
        config: Configuration object
        
    Returns:
        dict of time series arrays
    """
    n_snapshots = len(history)
    
    # Initialize arrays
    time_series = {
        'time': np.zeros(n_snapshots),
        'mean_speed': np.zeros(n_snapshots),
        'polarization': np.zeros(n_snapshots),
        'angular_momentum': np.zeros(n_snapshots),
        'mean_neighbors': np.zeros(n_snapshots),
    }
    
    # Add species-specific arrays if needed
    if hasattr(config, 'species1_label'):
        for species_label in [config.species1_label, config.species2_label]:
            prefix = f'species_{species_label}_'
            time_series[prefix + 'mean_speed'] = np.zeros(n_snapshots)
            time_series[prefix + 'polarization'] = np.zeros(n_snapshots)
    
    # Compute metrics for each snapshot
    for i, state in enumerate(history):
        time_series['time'][i] = i * config.dt * config.save_every
        metrics = compute_metrics(state, config)
        
        time_series['mean_speed'][i] = metrics['mean_speed']
        time_series['polarization'][i] = metrics['polarization']
        time_series['angular_momentum'][i] = metrics['angular_momentum']
        time_series['mean_neighbors'][i] = metrics['mean_neighbors']
        
        # Species-specific metrics
        if hasattr(config, 'species1_label'):
            for species_label in [config.species1_label, config.species2_label]:
                prefix = f'species_{species_label}_'
                if prefix + 'mean_speed' in metrics:
                    time_series[prefix + 'mean_speed'][i] = metrics[prefix + 'mean_speed']
                    time_series[prefix + 'polarization'][i] = metrics[prefix + 'polarization']
    
    return time_series


def compute_pair_correlation(positions, domain, r_max, n_bins=50):
    """
    Compute pair correlation function g(r).
    
    Args:
        positions: array of positions
        domain: Domain object
        r_max: maximum distance to compute
        n_bins: number of bins
        
    Returns:
        tuple of (r, g(r))
    """
    n_agents = len(positions)
    
    # Create bins
    bin_edges = np.linspace(0, r_max, n_bins + 1)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_width = bin_edges[1] - bin_edges[0]
    
    # Count pairs in each bin
    pair_counts = np.zeros(n_bins)
    
    for i in range(n_agents):
        for j in range(i + 1, n_agents):
            dist = domain.distance(positions[i], positions[j])
            if dist < r_max:
                bin_idx = int(dist / bin_width)
                if bin_idx < n_bins:
                    pair_counts[bin_idx] += 2  # Count both i-j and j-i
    
    # Normalize by ideal gas
    volume = np.prod(domain.size)
    density = n_agents / volume
    
    if domain.dimension == 2:
        shell_areas = np.pi * ((bin_edges[1:])**2 - (bin_edges[:-1])**2)
    else:  # 3D
        shell_volumes = (4.0/3.0) * np.pi * ((bin_edges[1:])**3 - (bin_edges[:-1])**3)
        shell_areas = shell_volumes
    
    ideal_counts = density * shell_areas * n_agents
    
    g_r = pair_counts / (ideal_counts + 1e-10)
    
    return bin_centers, g_r