"""
Implements boundary conditions (ground interaction).
Stage 2: Ground boundary with sticky condition.
"""
import numpy as np

def apply_boundary_conditions(state, velocities):
    """
    Apply boundary conditions to velocities.
    
    For Stage 2: Implement sticky ground boundary.
    - Locusts on ground (z=0) with downward velocity stay grounded (v=0)
    - Locusts on ground with upward velocity can take off
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    velocities : ndarray
        Computed velocities of shape (N, 2)
    
    Returns:
    --------
    ndarray
        Modified velocities of shape (N, 2)
    """
    modified_velocities = velocities.copy()
    
    # Check each locust
    for i in range(state.N):
        # If locust is on or below ground
        if state.positions[i, 1] <= 0:
            # Enforce ground level
            state.positions[i, 1] = 0
            
            # If vertical velocity is downward or zero, locust stays grounded
            if velocities[i, 1] <= 0:
                modified_velocities[i, :] = 0  # Set entire velocity to zero
                state.grounded[i] = True
            else:
                # Vertical velocity is positive, locust can take off
                state.grounded[i] = False
        else:
            # Locust is in the air
            state.grounded[i] = False
    
    return modified_velocities