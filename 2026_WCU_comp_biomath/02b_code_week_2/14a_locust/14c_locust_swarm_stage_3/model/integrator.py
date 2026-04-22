"""
Numerical time-stepping using Runge-Kutta 4th order (RK4).
"""
import numpy as np
from model.dynamics import compute_velocity

def rk4_step(state, dt, F, L, G, U):
    """
    Perform one RK4 time step.
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    dt : float
        Time step
    F, L, G, U : float
        Model parameters
    
    Returns:
    --------
    ndarray
        New positions of shape (N, 2)
    """
    # k1
    k1 = compute_velocity(state, F, L, G, U)
    
    # k2
    state_temp = state.copy()
    state_temp.positions = state.positions + 0.5 * dt * k1
    k2 = compute_velocity(state_temp, F, L, G, U)
    
    # k3
    state_temp.positions = state.positions + 0.5 * dt * k2
    k3 = compute_velocity(state_temp, F, L, G, U)
    
    # k4
    state_temp.positions = state.positions + dt * k3
    k4 = compute_velocity(state_temp, F, L, G, U)
    
    # Update positions
    new_positions = state.positions + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    
    return new_positions