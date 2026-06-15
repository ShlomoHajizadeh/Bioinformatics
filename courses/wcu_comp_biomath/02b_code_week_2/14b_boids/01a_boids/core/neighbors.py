"""
Neighbor finding for Reynolds boids simulation.
"""
import numpy as np


def find_neighbors(state, domain, radius, species_label=None):
    """
    Find neighbors within a given radius for each agent.
    
    Args:
        state: State object
        domain: Domain object
        radius: interaction radius
        species_label: if provided, only find neighbors of this species
        
    Returns:
        list: List of neighbor indices for each agent
    """
    positions = state.positions
    n_agents = state.n_agents
    
    # Filter by species if requested
    if species_label is not None:
        mask = state.get_species_mask(species_label)
        agent_indices = np.where(mask)[0]
    else:
        agent_indices = np.arange(n_agents)
    
    neighbors = []
    
    for i in range(n_agents):
        agent_neighbors = []
        
        for j in agent_indices:
            if i == j:
                continue
            
            # Compute distance with periodic boundaries
            delta = domain.minimum_image(positions[i] - positions[j])
            distance = np.linalg.norm(delta)
            
            if distance < radius:
                agent_neighbors.append(j)
        
        neighbors.append(agent_neighbors)
    
    return neighbors


def find_neighbors_efficient(state, domain, radius, species_label=None):
    """
    More efficient neighbor finding using vectorized operations.
    
    Args:
        state: State object
        domain: Domain object
        radius: interaction radius
        species_label: if provided, only find neighbors of this species
        
    Returns:
        list: List of neighbor indices for each agent
    """
    positions = state.positions
    n_agents = state.n_agents
    
    # Filter by species if requested
    if species_label is not None:
        mask = state.get_species_mask(species_label)
        candidate_indices = np.where(mask)[0]
    else:
        candidate_indices = np.arange(n_agents)
    
    neighbors = []
    
    for i in range(n_agents):
        # Compute all distances at once
        deltas = positions[candidate_indices] - positions[i]
        deltas = domain.minimum_image(deltas)
        distances = np.linalg.norm(deltas, axis=1)
        
        # Find neighbors (excluding self)
        neighbor_mask = (distances < radius) & (distances > 0)
        agent_neighbors = candidate_indices[neighbor_mask].tolist()
        
        neighbors.append(agent_neighbors)
    
    return neighbors


def find_neighbors_by_radius(state, domain, radii_dict):
    """
    Find neighbors for multiple radii at once.
    
    Args:
        state: State object
        domain: Domain object
        radii_dict: dict mapping radius names to values
                   e.g., {'avoidance': 5.0, 'alignment': 15.0}
        
    Returns:
        dict: Dictionary mapping radius names to neighbor lists
    """
    max_radius = max(radii_dict.values())
    
    # First find all neighbors within max radius
    all_neighbors = find_neighbors_efficient(state, domain, max_radius)
    
    # Precompute all distances
    positions = state.positions
    n_agents = state.n_agents
    
    result = {name: [[] for _ in range(n_agents)] for name in radii_dict}
    
    for i in range(n_agents):
        for j in all_neighbors[i]:
            delta = domain.minimum_image(positions[i] - positions[j])
            distance = np.linalg.norm(delta)
            
            # Assign to appropriate radius categories
            for name, radius in radii_dict.items():
                if distance < radius:
                    result[name][i].append(j)
    
    return result