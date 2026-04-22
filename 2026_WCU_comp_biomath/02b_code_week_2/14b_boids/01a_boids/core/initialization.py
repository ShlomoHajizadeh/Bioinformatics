"""
Initialization routines for Reynolds boids simulation.
"""
import numpy as np
from .state import State


def initialize_state(config):
    """
    Initialize the simulation state with random positions and velocities.
    
    Args:
        config: Configuration object (Config2D or Config3D)
        
    Returns:
        State: Initial state with random positions and velocities
    """
    n_agents = config.n_agents
    dimension = config.dimension
    domain_size = np.array(config.domain_size)
    
    # Initialize positions uniformly in domain
    positions = np.random.uniform(
        low=0.0,
        high=domain_size,
        size=(n_agents, dimension)
    )
    
    # Initialize velocities with random directions and magnitudes
    velocities = np.random.uniform(
        low=-config.v_init_max,
        high=config.v_init_max,
        size=(n_agents, dimension)
    )
    
    # Create species labels
    species = np.zeros(n_agents, dtype=np.int32)
    
    # First n_species1 agents are species 1 (label 0)
    # Remaining agents are species 2 (label 1)
    species[config.n_species1:] = config.species2_label
    
    # Create and return state
    state = State(positions, velocities, species)
    
    return state


def initialize_state_clustered(config, n_clusters=5):
    """
    Initialize state with agents clustered in space.
    
    Args:
        config: Configuration object
        n_clusters: number of initial clusters
        
    Returns:
        State: Initial state with clustered positions
    """
    n_agents = config.n_agents
    dimension = config.dimension
    domain_size = np.array(config.domain_size)
    
    # Generate cluster centers
    cluster_centers = np.random.uniform(
        low=0.0,
        high=domain_size,
        size=(n_clusters, dimension)
    )
    
    # Assign agents to clusters
    cluster_assignments = np.random.randint(0, n_clusters, size=n_agents)
    
    # Generate positions around cluster centers
    positions = np.zeros((n_agents, dimension))
    cluster_radius = np.min(domain_size) * 0.1  # 10% of smallest domain size
    
    for i in range(n_agents):
        cluster_idx = cluster_assignments[i]
        center = cluster_centers[cluster_idx]
        
        # Add random offset from cluster center
        offset = np.random.uniform(
            low=-cluster_radius,
            high=cluster_radius,
            size=dimension
        )
        
        positions[i] = center + offset
    
    # Wrap positions into domain
    positions = np.mod(positions, domain_size)
    
    # Initialize velocities with random directions
    velocities = np.random.uniform(
        low=-config.v_init_max,
        high=config.v_init_max,
        size=(n_agents, dimension)
    )
    
    # Create species labels
    species = np.zeros(n_agents, dtype=np.int32)
    species[config.n_species1:] = config.species2_label
    
    state = State(positions, velocities, species)
    
    return state


def initialize_state_ordered(config):
    """
    Initialize state with aligned velocities (ordered initial condition).
    
    Args:
        config: Configuration object
        
    Returns:
        State: Initial state with aligned velocities
    """
    n_agents = config.n_agents
    dimension = config.dimension
    domain_size = np.array(config.domain_size)
    
    # Random positions
    positions = np.random.uniform(
        low=0.0,
        high=domain_size,
        size=(n_agents, dimension)
    )
    
    # All velocities point in same direction with same magnitude
    base_direction = np.random.randn(dimension)
    base_direction = base_direction / np.linalg.norm(base_direction)
    
    velocities = np.tile(base_direction, (n_agents, 1)) * config.v_init_max
    
    # Add small random perturbations
    noise = np.random.randn(n_agents, dimension) * 0.1
    velocities += noise
    
    # Create species labels
    species = np.zeros(n_agents, dtype=np.int32)
    species[config.n_species1:] = config.species2_label
    
    state = State(positions, velocities, species)
    
    return state