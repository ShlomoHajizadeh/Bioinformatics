"""
Compute time series and spatial metrics for analysis.
"""

import numpy as np
from scipy.spatial.distance import pdist
from scipy.ndimage import label


def calculate_bison_dispersion(bison_positions, grid_size):
    """
    Calculate spatial dispersion index of bison.
    
    Args:
        bison_positions: List of (x, y) tuples
        grid_size: Tuple (nx, ny)
        
    Returns:
        float: Dispersion index (variance/mean ratio)
    """
    if len(bison_positions) == 0:
        return 0.0
    
    nx, ny = grid_size
    
    # Create density grid
    density = np.zeros((ny, nx))
    for x, y in bison_positions:
        density[y, x] += 1
    
    # Calculate dispersion (variance-to-mean ratio)
    mean_density = np.mean(density)
    var_density = np.var(density)
    
    if mean_density > 0:
        dispersion = var_density / mean_density
    else:
        dispersion = 0.0
    
    return dispersion


def calculate_mean_cluster_size(bison_positions, grid_size):
    """
    Calculate mean cluster size of bison using connected components.
    
    Args:
        bison_positions: List of (x, y) tuples
        grid_size: Tuple (nx, ny)
        
    Returns:
        float: Mean cluster size
    """
    if len(bison_positions) == 0:
        return 0.0
    
    nx, ny = grid_size
    
    # Create binary grid
    grid = np.zeros((ny, nx), dtype=int)
    for x, y in bison_positions:
        grid[y, x] = 1
    
    # Find connected components
    labeled_array, num_features = label(grid)
    
    if num_features == 0:
        return 0.0
    
    # Calculate cluster sizes
    cluster_sizes = []
    for i in range(1, num_features + 1):
        cluster_size = np.sum(labeled_array == i)
        cluster_sizes.append(cluster_size)
    
    return np.mean(cluster_sizes)


def calculate_pairwise_distances(bison_positions, grid_size):
    """
    Calculate pairwise distances between bison (accounting for toroidal topology).
    
    Args:
        bison_positions: List of (x, y) tuples
        grid_size: Tuple (nx, ny)
        
    Returns:
        numpy.ndarray: Array of pairwise distances
    """
    if len(bison_positions) < 2:
        return np.array([])
    
    nx, ny = grid_size
    positions = np.array(bison_positions)
    
    # Calculate toroidal distances
    distances = []
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            
            dx = min(abs(x2 - x1), nx - abs(x2 - x1))
            dy = min(abs(y2 - y1), ny - abs(y2 - y1))
            
            dist = np.sqrt(dx**2 + dy**2)
            distances.append(dist)
    
    return np.array(distances)


def calculate_spatial_autocorrelation(grass_stages, cell_types):
    """
    Calculate Moran's I for spatial autocorrelation of grass stages.
    
    Args:
        grass_stages: 2D array of grass stages
        cell_types: 2D array of cell types
        
    Returns:
        float: Moran's I statistic
    """
    ny, nx = grass_stages.shape
    
    # Get only grassland cells
    grass_mask = cell_types == "grass"
    grass_values = grass_stages[grass_mask]
    
    if len(grass_values) < 2:
        return 0.0
    
    # Simplified Moran's I calculation
    mean_val = np.mean(grass_values)
    
    # Calculate numerator and denominator
    numerator = 0.0
    denominator = 0.0
    total_weight = 0.0
    
    positions = np.argwhere(grass_mask)
    
    for i, (y1, x1) in enumerate(positions):
        val1 = grass_stages[y1, x1]
        
        for j, (y2, x2) in enumerate(positions):
            if i == j:
                continue
            
            # Simple adjacency weight (1 if neighbors, 0 otherwise)
            if abs(y1 - y2) + abs(x1 - x2) == 1:
                weight = 1.0
            else:
                weight = 0.0
            
            val2 = grass_stages[y2, x2]
            
            numerator += weight * (val1 - mean_val) * (val2 - mean_val)
            total_weight += weight
        
        denominator += (val1 - mean_val) ** 2
    
    if total_weight == 0 or denominator == 0:
        return 0.0
    
    n = len(grass_values)
    morans_i = (n / total_weight) * (numerator / denominator)
    
    return morans_i


def analyze_vegetation_dynamics(statistics):
    """
    Analyze vegetation dynamics from simulation statistics.
    
    Args:
        statistics: Statistics dictionary from simulation
        
    Returns:
        dict: Analysis results
    """
    results = {}
    
    # Forest growth rate
    forest_cells = np.array(statistics['forest_cells'])
    if len(forest_cells) > 1:
        forest_growth = np.diff(forest_cells)
        results['mean_forest_growth_rate'] = np.mean(forest_growth)
        results['total_forest_change'] = forest_cells[-1] - forest_cells[0]
        results['forest_growth_trend'] = np.polyfit(range(len(forest_cells)), forest_cells, 1)[0]
    
    # Grass stage stability
    grass_stages = np.array(statistics['mean_grass_stage'])
    if len(grass_stages) > 1:
        results['grass_stage_variance'] = np.var(grass_stages)
        results['final_grass_stage'] = grass_stages[-1]
        results['grass_stage_trend'] = np.polyfit(range(len(grass_stages)), grass_stages, 1)[0]
    
    # Overgrazing analysis
    overgrazed = np.array(statistics['overgrazed_cells'])
    if len(overgrazed) > 0:
        results['mean_overgrazed_cells'] = np.mean(overgrazed)
        results['max_overgrazed_cells'] = np.max(overgrazed)
        results['final_overgrazed_cells'] = overgrazed[-1]
    
    # Wolf-bison interaction frequency
    encounters = np.array(statistics['wolf_bison_encounters'])
    if len(encounters) > 0:
        results['total_encounters'] = np.sum(encounters)
        results['mean_encounters_per_step'] = np.mean(encounters)
        results['max_encounters'] = np.max(encounters)
    
    # Forest conversion analysis
    conversions = np.array(statistics['forest_conversions'])
    if len(conversions) > 0:
        results['total_conversions'] = np.sum(conversions)
        results['conversion_rate'] = np.sum(conversions) / len(conversions)
    
    return results


def compute_all_metrics(simulation):
    """
    Compute all metrics for a completed simulation.
    
    Args:
        simulation: Simulation object (after running)
        
    Returns:
        dict: All computed metrics
    """
    statistics = simulation.get_statistics()
    grid_size = (simulation.nx, simulation.ny)
    
    metrics = {
        'vegetation_dynamics': analyze_vegetation_dynamics(statistics),
        'bison_dispersion_timeseries': [],
        'cluster_size_timeseries': []
    }
    
    # Calculate time-varying metrics
    for bison_positions in statistics['bison_positions']:
        dispersion = calculate_bison_dispersion(bison_positions, grid_size)
        cluster_size = calculate_mean_cluster_size(bison_positions, grid_size)
        
        metrics['bison_dispersion_timeseries'].append(dispersion)
        metrics['cluster_size_timeseries'].append(cluster_size)
    
    # Final spatial autocorrelation
    metrics['final_spatial_autocorrelation'] = calculate_spatial_autocorrelation(
        simulation.environment.grass_stages,
        simulation.environment.cell_types
    )
    
    return metrics