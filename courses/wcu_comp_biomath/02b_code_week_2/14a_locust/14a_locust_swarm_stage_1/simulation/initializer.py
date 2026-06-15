"""
Creates initial swarm configurations.
"""
import numpy as np
from model.state import SwarmState

def random_cloud(N, domain_size, seed=None):
    """
    Initialize locusts in a random cloud.
    
    Parameters:
    -----------
    N : int
        Number of locusts
    domain_size : float
        Size of initialization domain
    seed : int, optional
        Random seed
    
    Returns:
    --------
    SwarmState
        Initial state
    """
    if seed is not None:
        np.random.seed(seed)
    
    state = SwarmState(N)
    state.positions = domain_size * (np.random.rand(N, 2) - 0.5)
    
    return state

def disk_swarm(N, radius, seed=None):
    """
    Initialize locusts in a disk-shaped swarm.
    
    Parameters:
    -----------
    N : int
        Number of locusts
    radius : float
        Disk radius
    seed : int, optional
        Random seed
    
    Returns:
    --------
    SwarmState
        Initial state
    """
    if seed is not None:
        np.random.seed(seed)
    
    state = SwarmState(N)
    
    for i in range(N):
        r = radius * np.sqrt(np.random.rand())
        theta = 2 * np.pi * np.random.rand()
        state.positions[i, 0] = r * np.cos(theta)
        state.positions[i, 1] = r * np.sin(theta)
    
    return state