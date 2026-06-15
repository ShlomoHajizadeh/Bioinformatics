"""
Implements gravity and wind contributions.
Stage 1: These are set to zero.
"""
import numpy as np

def gravity_contribution(N, G):
    """
    Compute gravity contribution to velocity.
    
    Parameters:
    -----------
    N : int
        Number of locusts
    G : float
        Gravity strength
    
    Returns:
    --------
    ndarray
        Gravity velocity of shape (N, 2)
    """
    gravity_vel = np.zeros((N, 2))
    gravity_vel[:, 1] = -G  # Negative z-direction
    return gravity_vel

def wind_contribution(N, U):
    """
    Compute wind contribution to velocity.
    
    Parameters:
    -----------
    N : int
        Number of locusts
    U : float
        Wind speed
    
    Returns:
    --------
    ndarray
        Wind velocity of shape (N, 2)
    """
    wind_vel = np.zeros((N, 2))
    wind_vel[:, 0] = U  # Positive x-direction
    return wind_vel