"""
Reynolds boids rules with predator-prey extensions.
"""
import numpy as np
from core.neighbors import find_neighbors_efficient


def separation(positions, neighbors, domain):
    """
    Separation rule: steer to avoid crowding neighbors.
    
    Args:
        positions: array of agent positions
        neighbors: list of neighbor indices for each agent
        domain: Domain object
        
    Returns:
        array of acceleration vectors
    """
    n_agents = len(positions)
    accelerations = np.zeros_like(positions)
    
    for i in range(n_agents):
        if len(neighbors[i]) > 0:
            # Get neighbor positions
            neighbor_positions = positions[neighbors[i]]
            
            # Compute vectors away from neighbors
            diff = positions[i] - neighbor_positions
            diff = domain.minimum_image_array(diff)
            
            # Weight by inverse distance
            distances = np.linalg.norm(diff, axis=1, keepdims=True)
            distances = np.maximum(distances, 1e-6)  # Avoid division by zero
            
            weighted_diff = diff / distances**2
            accelerations[i] = np.mean(weighted_diff, axis=0)
    
    return accelerations


def alignment(positions, velocities, neighbors, domain):
    """
    Alignment rule: steer towards average heading of neighbors.
    
    Args:
        positions: array of agent positions
        velocities: array of agent velocities
        neighbors: list of neighbor indices for each agent
        domain: Domain object
        
    Returns:
        array of acceleration vectors
    """
    n_agents = len(positions)
    accelerations = np.zeros_like(positions)
    
    for i in range(n_agents):
        if len(neighbors[i]) > 0:
            # Average velocity of neighbors
            neighbor_velocities = velocities[neighbors[i]]
            avg_velocity = np.mean(neighbor_velocities, axis=0)
            
            # Steer towards average velocity
            accelerations[i] = avg_velocity - velocities[i]
    
    return accelerations


def cohesion(positions, neighbors, domain):
    """
    Cohesion rule: steer towards average position of neighbors.
    
    Args:
        positions: array of agent positions
        neighbors: list of neighbor indices for each agent
        domain: Domain object
        
    Returns:
        array of acceleration vectors
    """
    n_agents = len(positions)
    accelerations = np.zeros_like(positions)
    
    for i in range(n_agents):
        if len(neighbors[i]) > 0:
            # Average position of neighbors
            neighbor_positions = positions[neighbors[i]]
            center_of_mass = np.mean(neighbor_positions, axis=0)
            
            # Steer towards center of mass
            diff = center_of_mass - positions[i]
            diff = domain.minimum_image(diff)
            accelerations[i] = diff
    
    return accelerations


def interspecies_avoidance(positions, species, neighbors_other_species, domain, species_label):
    """
    Interspecies avoidance: prey avoid predators.
    
    Args:
        positions: array of all agent positions
        species: array of species labels
        neighbors_other_species: list of other-species neighbor indices
        domain: Domain object
        species_label: label of species being computed
        
    Returns:
        array of acceleration vectors for this species
    """
    mask = species == species_label
    n_agents_species = np.sum(mask)
    accelerations = np.zeros((n_agents_species, positions.shape[1]))
    
    species_indices = np.where(mask)[0]
    
    for idx, i in enumerate(species_indices):
        if len(neighbors_other_species[i]) > 0:
            # Get predator positions
            predator_positions = positions[neighbors_other_species[i]]
            
            # Compute vectors away from predators
            diff = positions[i] - predator_positions
            diff = domain.minimum_image_array(diff)
            
            # Weight by inverse distance squared (stronger avoidance when closer)
            distances = np.linalg.norm(diff, axis=1, keepdims=True)
            distances = np.maximum(distances, 1e-6)
            
            weighted_diff = diff / distances**2
            accelerations[idx] = np.mean(weighted_diff, axis=0)
    
    return accelerations


def hunting(positions, species, domain, hunter_species_label, prey_species_label):
    """
    Hunting behavior: predators pursue prey center of mass.
    
    Args:
        positions: array of all agent positions
        species: array of species labels
        domain: Domain object
        hunter_species_label: label of predator species
        prey_species_label: label of prey species
        
    Returns:
        array of acceleration vectors for predators
    """
    hunter_mask = species == hunter_species_label
    prey_mask = species == prey_species_label
    
    n_hunters = np.sum(hunter_mask)
    accelerations = np.zeros((n_hunters, positions.shape[1]))
    
    if np.sum(prey_mask) == 0:
        return accelerations
    
    # Compute prey center of mass
    prey_positions = positions[prey_mask]
    prey_center = np.mean(prey_positions, axis=0)
    
    hunter_indices = np.where(hunter_mask)[0]
    hunter_positions = positions[hunter_mask]
    
    for idx, i in enumerate(hunter_indices):
        # Vector toward prey center
        diff = prey_center - hunter_positions[idx]
        diff = domain.minimum_image(diff)
        
        distance = np.linalg.norm(diff)
        if distance > 1e-6:
            # Normalize and scale by distance (weaker at distance)
            accelerations[idx] = diff / distance
    
    return accelerations


def apply_velocity_limits(velocities, species, config):
    """
    Apply species-specific velocity limits.
    
    Args:
        velocities: array of velocity vectors
        species: array of species labels
        config: Configuration object
        
    Returns:
        array of limited velocity vectors
    """
    limited_velocities = velocities.copy()
    
    # Check if multi-species
    if hasattr(config, 'species1_label') and hasattr(config, 'species2_label'):
        # Species 1 (prey)
        mask1 = species == config.species1_label
        if np.any(mask1):
            speeds = np.linalg.norm(velocities[mask1], axis=1, keepdims=True)
            speeds = np.clip(speeds, config.v_min, config.v_max)
            directions = velocities[mask1] / (np.linalg.norm(velocities[mask1], axis=1, keepdims=True) + 1e-10)
            limited_velocities[mask1] = directions * speeds
        
        # Species 2 (predators)
        mask2 = species == config.species2_label
        if np.any(mask2):
            speeds = np.linalg.norm(velocities[mask2], axis=1, keepdims=True)
            speeds = np.clip(speeds, config.v_min_sp2, config.v_max_sp2)
            directions = velocities[mask2] / (np.linalg.norm(velocities[mask2], axis=1, keepdims=True) + 1e-10)
            limited_velocities[mask2] = directions * speeds
    else:
        # Single species
        speeds = np.linalg.norm(velocities, axis=1, keepdims=True)
        speeds = np.clip(speeds, config.v_min, config.v_max)
        directions = velocities / (speeds + 1e-10)
        limited_velocities = directions * speeds
    
    return limited_velocities


def compute_accelerations(state, domain, config):
    """
    Compute accelerations for all agents based on Reynolds rules.
    Handles multi-species predator-prey dynamics.
    
    Args:
        state: State object
        domain: Domain object
        config: Configuration object
        
    Returns:
        array of acceleration vectors
    """
    n_agents = state.n_agents
    accelerations = np.zeros_like(state.positions)
    
    # Check if multi-species simulation
    is_multispecies = hasattr(config, 'species1_label') and hasattr(config, 'species2_label')
    
    if not is_multispecies:
        # Single species - standard boids
        # Find neighbors for each rule
        neighbors_avoid = find_neighbors_efficient(state.positions, domain, config.r_avoid)
        neighbors_align = find_neighbors_efficient(state.positions, domain, config.r_align)
        neighbors_cohesion = find_neighbors_efficient(state.positions, domain, config.r_cohesion)
        
        # Compute rule contributions
        acc_avoid = separation(state.positions, neighbors_avoid, domain)
        acc_align = alignment(state.positions, state.velocities, neighbors_align, domain)
        acc_cohesion = cohesion(state.positions, neighbors_cohesion, domain)
        
        # Combine with weights
        accelerations = (config.w_avoid * acc_avoid +
                        config.w_align * acc_align +
                        config.w_cohesion * acc_cohesion)
    
    else:
        # Multi-species predator-prey
        species1_mask = state.species == config.species1_label
        species2_mask = state.species == config.species2_label
        
        # === SPECIES 1 (PREY) ===
        if np.any(species1_mask):
            # Get prey positions and velocities
            prey_positions = state.positions[species1_mask]
            prey_velocities = state.velocities[species1_mask]
            
            # Find same-species neighbors for boids rules
            neighbors_avoid = find_neighbors_efficient(prey_positions, domain, config.r_avoid)
            neighbors_align = find_neighbors_efficient(prey_positions, domain, config.r_align)
            neighbors_cohesion = find_neighbors_efficient(prey_positions, domain, config.r_cohesion)
            
            # Compute boids rules for prey
            acc_avoid = separation(prey_positions, neighbors_avoid, domain)
            acc_align = alignment(prey_positions, prey_velocities, neighbors_align, domain)
            acc_cohesion = cohesion(prey_positions, neighbors_cohesion, domain)
            
            # Find predator neighbors for avoidance
            neighbors_predators = find_neighbors_efficient(
                state.positions, domain, config.r_avoid_interspecies
            )
            
            # Filter to only predators
            for i in range(len(neighbors_predators)):
                neighbors_predators[i] = [n for n in neighbors_predators[i] 
                                         if state.species[n] == config.species2_label]
            
            # Compute predator avoidance
            acc_avoid_predators = interspecies_avoidance(
                state.positions, state.species, neighbors_predators, 
                domain, config.species1_label
            )
            
            # Combine all forces for prey
            acc_sp1 = (config.w_avoid * acc_avoid +
                      config.w_align * acc_align +
                      config.w_cohesion * acc_cohesion +
                      config.w_avoidance_interspecies * acc_avoid_predators)
            
            accelerations[species1_mask] = acc_sp1
        
        # === SPECIES 2 (PREDATORS) ===
        if np.any(species2_mask):
            # Get predator positions
            predator_positions = state.positions[species2_mask]
            
            # Find same-species neighbors for separation
            neighbors_avoid_sp2 = find_neighbors_efficient(
                predator_positions, domain, config.r_avoid_sp2
            )
            
            # Compute separation for predators
            acc_avoid_sp2 = separation(predator_positions, neighbors_avoid_sp2, domain)
            
            # Compute hunting behavior
            acc_hunt = hunting(
                state.positions, state.species, domain,
                config.species2_label, config.species1_label
            )
            
            # Combine forces for predators
            acc_sp2 = (config.w_avoid_sp2 * acc_avoid_sp2 +
                      config.w_hunt * acc_hunt)
            
            accelerations[species2_mask] = acc_sp2
    
    return accelerations