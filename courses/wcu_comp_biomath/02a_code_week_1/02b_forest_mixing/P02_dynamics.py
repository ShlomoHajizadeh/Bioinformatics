"""
dynamics.py

Functions for simulating the forest dynamics with Moore neighborhood.

Boundary Condition: FIXED (NON-PERIODIC) BOUNDARIES
The lattice represents a finite plot of land with edges.
Edge and corner cells have fewer neighbors:
- Corner cells: 3 neighbors
- Edge cells (non-corner): 5 neighbors
- Interior cells: 8 neighbors

This models a real farmer's plot where there are physical boundaries.
"""

import numpy as np


def get_moore_neighborhood(lattice, i, j):
    """
    Get the Moore neighborhood of cell (i, j) with FIXED boundaries.
    
    The Moore neighborhood includes up to 8 surrounding cells:
        NW  N  NE
        W   X  E
        SW  S  SE
    
    where X is the cell at (i, j).
    
    For cells at the edges or corners, only existing neighbors are returned.
    This means:
    - Corner cells have 3 neighbors
    - Edge cells have 5 neighbors
    - Interior cells have 8 neighbors
    
    Parameters
    ----------
    lattice : numpy.ndarray
        Current lattice state (N x N array).
    i : int
        Row index of the cell.
    j : int
        Column index of the cell.
    
    Returns
    -------
    neighbors : list of int
        List of neighbor states (each is 0 for RO or 1 for HI).
        Length varies from 3 (corner) to 8 (interior).
    """
    N = lattice.shape[0]
    neighbors = []
    
    # Define the 8 possible neighbor positions (relative offsets)
    # Order: NW, N, NE, W, E, SW, S, SE
    offsets = [
        (-1, -1), (-1, 0), (-1, 1),  # Top row: NW, N, NE
        (0, -1),           (0, 1),    # Middle row: W, E
        (1, -1),  (1, 0),  (1, 1)     # Bottom row: SW, S, SE
    ]
    
    # Check each potential neighbor
    for di, dj in offsets:
        ni, nj = i + di, j + dj
        
        # Only include neighbor if it's within bounds
        if 0 <= ni < N and 0 <= nj < N:
            neighbors.append(lattice[ni, nj])
    
    return neighbors


def update_cell_with_neighbors(current_state, neighbors, transition_probabilities, rng):
    """
    Update a single cell based on its current state and neighbors.
    
    Update rules:
    - If current cell is RO (0):
        * If ALL neighbors are RO: stay RO with probability 1.0
        * Otherwise: RO with prob 0.50, HI with prob 0.50
    
    - If current cell is HI (1):
        * If ALL neighbors are HI: stay HI with probability 1.0
        * Otherwise: RO with prob 0.74, HI with prob 0.26
    
    Note: For edge and corner cells with fewer neighbors, the rule still applies
    to whatever neighbors exist.
    
    Parameters
    ----------
    current_state : int
        Current species in the cell (0 = RO, 1 = HI).
    neighbors : list of int
        List of neighbor states (length varies: 3-8 depending on position).
    transition_probabilities : dict
        Dictionary with transition rules.
        Format: {state: [P(->RO), P(->HI)]}
    rng : numpy.random.Generator
        Random number generator.
    
    Returns
    -------
    new_state : int
        New species after transition.
    """
    # Handle edge case: if no neighbors (shouldn't happen with proper lattice)
    if len(neighbors) == 0:
        return current_state
    
    # Check if all neighbors are the same species as current cell
    all_same = all(neighbor == current_state for neighbor in neighbors)
    
    if all_same:
        # If all neighbors match current state, stay in current state
        new_state = current_state
    else:
        # Otherwise, apply stochastic transition rule
        probs = transition_probabilities[current_state]
        new_state = rng.choice([0, 1], p=probs)
    
    return new_state


def simulation_step(lattice, transition_probabilities, rng):
    """
    Perform one time step of the simulation with Moore neighborhood.
    
    Uses SYNCHRONOUS updating: all cells are updated simultaneously based
    on the current state of the lattice. This means:
    1. Read the current state of all cells
    2. Compute new states for all cells based on current state
    3. Update all cells to their new states
    
    Edge and corner cells have fewer neighbors but follow the same rules.
    
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
    
    # Update each cell based on its neighbors in the CURRENT lattice
    for i in range(N):
        for j in range(N):
            current_state = lattice[i, j]
            neighbors = get_moore_neighborhood(lattice, i, j)
            new_lattice[i, j] = update_cell_with_neighbors(
                current_state, neighbors, transition_probabilities, rng
            )
    
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
        Format: {state: [P(->RO), P(->HI)]}
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