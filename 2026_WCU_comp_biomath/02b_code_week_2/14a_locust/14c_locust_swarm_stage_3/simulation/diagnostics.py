"""
Computes diagnostic quantities for analysis.
"""
import numpy as np

def compute_diagnostics(state):
    """
    Compute diagnostic quantities for the swarm.
    
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
    
    # Airborne positions only (for some metrics)
    airborne = ~grounded
    airborne_positions = positions[airborne] if np.any(airborne) else positions
    
    # Basic statistics
    center = np.mean(positions, axis=0)
    
    # Swarm extent
    if len(positions) > 0:
        width = np.max(positions[:, 0]) - np.min(positions[:, 0])
        height = np.max(positions[:, 1]) - np.min(positions[:, 1])
    else:
        width = 0
        height = 0
    
    # Mean height (all locusts)
    mean_height = np.mean(positions[:, 1])
    
    # Mean height (airborne only)
    if np.any(airborne):
        mean_height_airborne = np.mean(airborne_positions[:, 1])
    else:
        mean_height_airborne = 0
    
    # Grounded count
    grounded_count = np.sum(grounded)
    
    # Horizontal spread (standard deviation in x)
    std_x = np.std(positions[:, 0])
    
    # Vertical spread (standard deviation in z)
    std_z = np.std(positions[:, 1])
    
    diagnostics = {
        'center_x': center[0],
        'center_z': center[1],
        'width': width,
        'height': height,
        'mean_height': mean_height,
        'mean_height_airborne': mean_height_airborne,
        'grounded_count': grounded_count,
        'airborne_count': state.N - grounded_count,
        'std_x': std_x,
        'std_z': std_z,
    }
    
    return diagnostics

def compute_rolling_diagnostics(state, velocities):
    """
    Compute diagnostics specific to rolling behavior (Stage 3).
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    velocities : ndarray
        Current velocities, shape (N, 2)
    
    Returns:
    --------
    dict
        Dictionary of rolling-specific diagnostics
    """
    grounded = state.grounded
    
    if np.any(grounded):
        # Velocities of grounded locusts
        grounded_velocities = velocities[grounded]
        
        # Mean horizontal velocity of grounded locusts (rolling speed)
        mean_rolling_speed = np.mean(grounded_velocities[:, 0])
        
        # Number of locusts actively rolling (horizontal velocity > threshold)
        rolling_threshold = 0.1
        rolling_count = np.sum(np.abs(grounded_velocities[:, 0]) > rolling_threshold)
    else:
        mean_rolling_speed = 0
        rolling_count = 0
    
    # Mean horizontal velocity of all locusts
    mean_horizontal_velocity = np.mean(velocities[:, 0])
    
    # Swarm front position (rightmost locust)
    front_position = np.max(state.positions[:, 0])
    
    # Swarm rear position (leftmost locust)
    rear_position = np.min(state.positions[:, 0])
    
    rolling_diagnostics = {
        'mean_rolling_speed': mean_rolling_speed,
        'rolling_count': rolling_count,
        'mean_horizontal_velocity': mean_horizontal_velocity,
        'front_position': front_position,
        'rear_position': rear_position,
        'swarm_length': front_position - rear_position,
    }
    
    return rolling_diagnostics