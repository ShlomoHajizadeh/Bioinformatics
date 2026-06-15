"""
initialization.py

Functions to generate the initial lattice for the forest model.
"""

import numpy as np


def create_random_lattice(N, p_RO=0.5, seed=None):
    """
    Create an N x N lattice with random initial distribution of species.
    
    Parameters
    ----------
    N : int
        Lattice size (N x N grid).
    p_RO : float, optional
        Probability that a cell is initially Red Oak (RO). Default is 0.5.
    seed : int or None, optional
        Random seed for reproducibility.
    
    Returns
    -------
    lattice : numpy.ndarray
        N x N array where 0 = Red Oak (RO), 1 = Hickory (HI).
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate random values between 0 and 1
    random_values = np.random.rand(N, N)
    
    # Assign species: 0 for RO (if random < p_RO), 1 for HI (otherwise)
    lattice = (random_values >= p_RO).astype(int)
    
    return lattice


def create_uniform_lattice(N, species=0):
    """
    Create an N x N lattice with a single species.
    
    Parameters
    ----------
    N : int
        Lattice size (N x N grid).
    species : int, optional
        Species code: 0 = Red Oak (RO), 1 = Hickory (HI). Default is 0.
    
    Returns
    -------
    lattice : numpy.ndarray
        N x N array filled with the specified species.
    """
    return np.full((N, N), species, dtype=int)


def create_checkerboard_lattice(N):
    """
    Create an N x N lattice with a checkerboard pattern.
    
    Parameters
    ----------
    N : int
        Lattice size (N x N grid).
    
    Returns
    -------
    lattice : numpy.ndarray
        N x N array with alternating RO (0) and HI (1).
    """
    lattice = np.zeros((N, N), dtype=int)
    lattice[1::2, ::2] = 1  # Odd rows, even columns
    lattice[::2, 1::2] = 1  # Even rows, odd columns
    return lattice


def create_half_split_lattice(N):
    """
    Create an N x N lattice split horizontally into two regions.
    
    Upper half (rows 0 to N//2-1): Hickory (HI) only
    Lower half (rows N//2 to N-1): Red Oak (RO) only
    
    This creates a "two-plantation" initial condition where the two species
    are spatially segregated.
    
    Parameters
    ----------
    N : int
        Lattice size (N x N grid).
    
    Returns
    -------
    lattice : numpy.ndarray
        N x N array where upper half is HI (1) and lower half is RO (0).
    """
    lattice = np.zeros((N, N), dtype=int)
    
    # Upper half: Hickory (HI = 1)
    lattice[:N//2, :] = 1
    
    # Lower half: Red Oak (RO = 0)
    lattice[N//2:, :] = 0
    
    return lattice