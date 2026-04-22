"""
High-level function to compute total velocity.
"""
import numpy as np
from model.interactions import compute_social_velocity
from model.forces import gravity_contribution, wind_contribution
from model.boundary import apply_boundary_conditions

def compute_velocity(state, F, L, G, U):
    """
    Compute total velocity for all locusts.
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    F : float
        Attraction strength
    L : float
        Attraction length scale
    G : float
        Gravity strength
    U : float
        Wind speed
    
    Returns:
    --------
    ndarray
        Total velocities of shape (N, 2)
    """
    N = state.N
    
    # Social interactions
    social_vel = compute_social_velocity(state.positions, F, L)
    
    # Gravity
    gravity_vel = gravity_contribution(N, G)
    
    # Wind
    wind_vel = wind_contribution(N, U)
    
    # Combined unconstrained velocity
    velocities = social_vel + gravity_vel + wind_vel
    
    # Apply boundary conditions
    velocities = apply_boundary_conditions(state, velocities)
    
    return velocities