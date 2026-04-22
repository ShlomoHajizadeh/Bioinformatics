"""
Computes diagnostic quantities for the swarm.
"""
import numpy as np

def compute_diagnostics(state):
    """
    Compute diagnostic statistics.
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    
    Returns:
    --------
    dict
        Dictionary of diagnostic values
    """
    positions = state.positions
    grounded = state.grounded
    
    # Mean height
    mean_height = np.mean(positions[:, 1])
    
    # Grounded count
    grounded_count = np.sum(grounded)
    
    # Swarm center
    center_x = np.mean(positions[:, 0])
    center_z = np.mean(positions[:, 1])
    
    # Width and height (range in x and z)
    width = np.max(positions[:, 0]) - np.min(positions[:, 0])
    height = np.max(positions[:, 1]) - np.min(positions[:, 1])
    
    # Pair distance statistics
    distances = []
    N = state.N
    for i in range(N):
        for j in range(i + 1, N):
            dist = np.linalg.norm(positions[j] - positions[i])
            distances.append(dist)
    
    if distances:
        mean_distance = np.mean(distances)
        min_distance = np.min(distances)
        max_distance = np.max(distances)
    else:
        mean_distance = 0.0
        min_distance = 0.0
        max_distance = 0.0
    
    return {
        'mean_height': mean_height,
        'grounded_count': grounded_count,
        'center_x': center_x,
        'center_z': center_z,
        'width': width,
        'height': height,
        'mean_distance': mean_distance,
        'min_distance': min_distance,
        'max_distance': max_distance
    }