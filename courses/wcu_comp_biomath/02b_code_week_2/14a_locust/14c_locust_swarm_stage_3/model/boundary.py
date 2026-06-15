"""
Implements boundary conditions (ground interaction).
Stage 3: Ground boundary with rolling behavior.
"""
import numpy as np

def apply_boundary_conditions(state, velocities):
    """
    Apply boundary conditions to velocities.
    
    For Stage 3: Implement ground boundary with rolling.
    - Locusts on ground (z=0) can roll horizontally due to wind
    - Vertical velocity is suppressed when grounded
    - Locusts can take off if vertical velocity becomes positive
    
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
            # ENFORCE ground level (critical fix)
            state.positions[i, 1] = 0
            
            # If vertical velocity is downward or zero
            if velocities[i, 1] <= 0:
                # Locust stays grounded
                state.grounded[i] = True
                
                # Allow horizontal rolling, suppress vertical motion
                modified_velocities[i, 0] = velocities[i, 0]  # Keep horizontal velocity
                modified_velocities[i, 1] = 0  # No vertical motion
            else:
                # Vertical velocity is positive, locust can take off
                state.grounded[i] = False
                # Keep full velocity for takeoff
        else:
            # Locust is in the air
            state.grounded[i] = False
    
    return modified_velocities