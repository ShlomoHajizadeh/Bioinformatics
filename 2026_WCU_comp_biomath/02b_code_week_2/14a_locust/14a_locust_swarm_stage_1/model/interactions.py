"""
Implements social interactions between locusts.
"""
import numpy as np

def morse_interaction(r, F, L):
    """
    Morse-type interaction function.
    
    Parameters:
    -----------
    r : float or ndarray
        Distance(s) between locusts
    F : float
        Attraction strength
    L : float
        Attraction length scale
    
    Returns:
    --------
    float or ndarray
        Social force magnitude s(r)
    """
    return F * np.exp(-r / L) - np.exp(-r)

def pairwise_distances(positions):
    """
    Compute pairwise distances between all locusts.
    
    Parameters:
    -----------
    positions : ndarray
        Array of shape (N, 2) containing positions
    
    Returns:
    --------
    ndarray
        Distance matrix of shape (N, N)
    """
    N = positions.shape[0]
    distances = np.zeros((N, N))
    
    for i in range(N):
        for j in range(i + 1, N):
            diff = positions[j] - positions[i]
            dist = np.linalg.norm(diff)
            distances[i, j] = dist
            distances[j, i] = dist
    
    return distances

def compute_social_velocity(positions, F, L):
    """
    Compute social velocity for each locust.
    
    Parameters:
    -----------
    positions : ndarray
        Array of shape (N, 2) containing positions
    F : float
        Attraction strength
    L : float
        Attraction length scale
    
    Returns:
    --------
    ndarray
        Social velocities of shape (N, 2)
    """
    N = positions.shape[0]
    social_vel = np.zeros((N, 2))
    
    for i in range(N):
        for j in range(N):
            if i != j:
                diff = positions[j] - positions[i]
                r = np.linalg.norm(diff)
                
                if r > 1e-10:  # Avoid division by zero
                    r_hat = diff / r
                    s = morse_interaction(r, F, L)
                    social_vel[i] += s * r_hat
    
    return social_vel