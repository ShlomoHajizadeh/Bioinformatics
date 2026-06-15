"""
Reynolds flocking rules: avoidance, alignment, and cohesion.
"""
import numpy as np


def compute_avoidance(state, domain, neighbors, radius):
    """
    Compute avoidance force (move away from nearby neighbors).
    
    Args:
        state: State object
        domain: Domain object
        neighbors: list of neighbor indices for each agent
        radius: avoidance radius
        
    Returns:
        ndarray: (n_agents, dimension) array of avoidance accelerations
    """
    n_agents = state.n_agents
    dimension = state.dimension
    positions = state.positions
    
    avoidance = np.zeros((n_agents, dimension))
    
    for i in range(n_agents):
        if not neighbors[i]:
            continue
        
        # Compute repulsion from each neighbor
        for j in neighbors[i]:
            delta = domain.minimum_image(positions[i] - positions[j])
            distance = np.linalg.norm(delta)
            
            if distance > 0 and distance < radius:
                # Repulsion inversely proportional to distance
                # Stronger when closer
                repulsion_strength = (radius - distance) / radius
                direction = delta / distance  # normalized
                avoidance[i] += direction * repulsion_strength
    
    return avoidance


def compute_alignment(state, domain, neighbors):
    """
    Compute alignment force (match velocity with neighbors).
    
    Args:
        state: State object
        domain: Domain object
        neighbors: list of neighbor indices for each agent
        
    Returns:
        ndarray: (n_agents, dimension) array of alignment accelerations
    """
    n_agents = state.n_agents
    dimension = state.dimension
    velocities = state.velocities
    
    alignment = np.zeros((n_agents, dimension))
    
    for i in range(n_agents):
        if not neighbors[i]:
            continue
        
        # Average velocity of neighbors
        neighbor_velocities = velocities[neighbors[i]]
        avg_velocity = np.mean(neighbor_velocities, axis=0)
        
        # Alignment is the difference between average and current velocity
        alignment[i] = avg_velocity - velocities[i]
    
    return alignment


def compute_cohesion(state, domain, neighbors):
    """
    Compute cohesion force (move toward center of mass of neighbors).
    
    Args:
        state: State object
        domain: Domain object
        neighbors: list of neighbor indices for each agent
        
    Returns:
        ndarray: (n_agents, dimension) array of cohesion accelerations
    """
    n_agents = state.n_agents
    dimension = state.dimension
    positions = state.positions
    
    cohesion = np.zeros((n_agents, dimension))
    
    for i in range(n_agents):
        if not neighbors[i]:
            continue
        
        # Compute center of mass of neighbors (with periodic boundaries)
        # This is tricky with periodic boundaries
        center = compute_periodic_center_of_mass(
            positions[i],
            positions[neighbors[i]],
            domain
        )
        
        # Direction toward center
        delta = domain.minimum_image(center - positions[i])
        cohesion[i] = delta
    
    return cohesion


def compute_periodic_center_of_mass(reference_pos, neighbor_positions, domain):
    """
    Compute center of mass of neighbors accounting for periodic boundaries.
    
    Uses the reference position to unwrap periodic positions.
    
    Args:
        reference_pos: position of the reference agent
        neighbor_positions: (n_neighbors, dimension) array
        domain: Domain object
        
    Returns:
        ndarray: center of mass position
    """
    if len(neighbor_positions) == 0:
        return reference_pos
    
    # Unwrap positions relative to reference
    deltas = neighbor_positions - reference_pos
    deltas = domain.minimum_image(deltas)
    unwrapped = reference_pos + deltas
    
    # Compute center of mass
    center = np.mean(unwrapped, axis=0)
    
    # Wrap back into domain
    center = domain.wrap(center.reshape(1, -1))[0]
    
    return center


def compute_accelerations(state, domain, config):
    """
    Compute accelerations for all agents based on Reynolds rules.
    
    Args:
        state: State object
        domain: Domain object
        config: Configuration object
        
    Returns:
        ndarray: (n_agents, dimension) array of accelerations
    """
    n_agents = state.n_agents
    dimension = state.dimension
    
    accelerations = np.zeros((n_agents, dimension))
    
    # Process each species separately
    for species_label in [config.species1_label, config.species2_label]:
        params = config.get_species_params(species_label)
        mask = state.get_species_mask(species_label)
        indices = np.where(mask)[0]
        
        if len(indices) == 0:
            continue
        
        # Find neighbors for different rules
        from .neighbors import find_neighbors_efficient
        
        # Avoidance neighbors (all agents)
        neighbors_avoid = find_neighbors_efficient(
            state, domain, params['r_avoidance']
        )
        
        # Compute avoidance for this species
        avoid_acc = compute_avoidance(
            state, domain, neighbors_avoid, params['r_avoidance']
        )
        
        accelerations += params['w_avoidance'] * avoid_acc
        
        # If full rules (species 1), add alignment and cohesion
        if params['full_rules']:
            # Alignment neighbors (same species only)
            neighbors_align = find_neighbors_efficient(
                state, domain, params['r_alignment'], species_label
            )
            
            # Cohesion neighbors (same species only)
            neighbors_cohesion = find_neighbors_efficient(
                state, domain, params['r_cohesion'], species_label
            )
            
            # Compute alignment and cohesion
            align_acc = compute_alignment(state, domain, neighbors_align)
            cohesion_acc = compute_cohesion(state, domain, neighbors_cohesion)
            
            # Add weighted contributions (only for this species)
            for i in indices:
                accelerations[i] += (
                    params['w_alignment'] * align_acc[i] +
                    params['w_cohesion'] * cohesion_acc[i]
                )
    
    return accelerations