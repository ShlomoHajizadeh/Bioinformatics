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

def airborne_cloud(N, domain_size, initial_height, seed=None):
    """
    Initialize locusts in a cloud above ground.
    
    Parameters:
    -----------
    N : int
        Number of locusts
    domain_size : float
        Horizontal size of initialization domain
    initial_height : float
        Mean height above ground
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
    
    # Random horizontal positions
    state.positions[:, 0] = domain_size * (np.random.rand(N) - 0.5)
    
    # Random vertical positions around initial_height
    state.positions[:, 1] = initial_height + 0.5 * domain_size * (np.random.rand(N) - 0.5)
    
    # Ensure all locusts start above ground
    state.positions[:, 1] = np.maximum(state.positions[:, 1], 0.1)
    
    return state

def airborne_disk(N, radius, center_height, seed=None):
    """
    Initialize locusts in a disk-shaped swarm above ground.
    
    Parameters:
    -----------
    N : int
        Number of locusts
    radius : float
        Disk radius
    center_height : float
        Height of disk center above ground
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
        state.positions[i, 1] = center_height + r * np.sin(theta)
    
    # Ensure all locusts start above ground
    state.positions[:, 1] = np.maximum(state.positions[:, 1], 0.1)
    
    return state
