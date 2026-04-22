"""
dynamics.py

Functions for simulating the forest dynamics.
"""

import numpy as np


def update_cell(current_state, transition_probabilities, rng):
    """
    Update a single cell according to transition probabilities.
    
    Parameters
    ----------
    current_state : int
        Current species in the cell (0 = RO, 1 = HI).
    transition_probabilities : dict
        Dictionary with transition rules.
        Example: {0: [0.5, 0.5], 1: [0.74, 0.26]}
        where transition_probabilities[state] = [P(->RO), P(->HI)]
    rng : numpy.random.Generator
        Random number generator.
    
    Returns
    -------
    new_state : int
        New species after transition.
    """
    # Get transition probabilities for current state
    probs = transition_probabilities[current_state]
    
    # Randomly choose new state based on probabilities
    # probs[0] = probability of becoming RO (state 0)
    # probs[1] = probability of becoming HI (state 1)
    new_state = rng.choice([0, 1], p=probs)
    
    return new_state


def simulation_step(lattice, transition_probabilities, rng):
    """
    Perform one time step of the simulation.
    
    Parameters
    ----------
    lattice : numpy.ndarray
        Current lattice state (N x N array).
    transition_probabilities : dict
        Transition rules for each species.
    rng : numpy.random.Generator
        Random number generator.
    
    Returns
    -------
    new_lattice : numpy.ndarray
        Updated lattice after one time step.
    """
    N = lattice.shape[0]
    new_lattice = np.zeros_like(lattice)
    
    # Update each cell independently
    for i in range(N):
        for j in range(N):
            current_state = lattice[i, j]
            new_lattice[i, j] = update_cell(current_state, transition_probabilities, rng)
    
    return new_lattice


def run_simulation(initial_lattice, T, transition_probabilities, seed=None):
    """
    Run the full simulation for T time steps.
    
    Parameters
    ----------
    initial_lattice : numpy.ndarray
        Initial lattice configuration.
    T : int
        Number of time steps.
    transition_probabilities : dict
        Transition rules for each species.
    seed : int or None, optional
        Random seed for reproducibility.
    
    Returns
    -------
    history : list of numpy.ndarray
        List containing lattice state at each time step (including initial state).
    counts_history : numpy.ndarray
        Array of shape (T+1, 2) containing counts of [RO, HI] at each time step.
    """
    # Initialize random number generator
    rng = np.random.default_rng(seed)
    
    # Store initial state
    history = [initial_lattice.copy()]
    
    # Count species at each time step
    N = initial_lattice.shape[0]
    total_cells = N * N
    counts_history = np.zeros((T + 1, 2), dtype=int)
    
    # Count initial species
    counts_history[0, 0] = np.sum(initial_lattice == 0)  # RO count
    counts_history[0, 1] = np.sum(initial_lattice == 1)  # HI count
    
    # Run simulation
    current_lattice = initial_lattice.copy()
    for t in range(T):
        current_lattice = simulation_step(current_lattice, transition_probabilities, rng)
        history.append(current_lattice.copy())
        
        # Count species
        counts_history[t + 1, 0] = np.sum(current_lattice == 0)  # RO
        counts_history[t + 1, 1] = np.sum(current_lattice == 1)  # HI
    
    return history, counts_history