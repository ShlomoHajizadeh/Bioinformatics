"""
Initialization functions for Reynolds boids simulation.
"""
import numpy as np
from core.state import State


def initialize_state(config):
    """
    Initialize the state of the boids simulation.
    
    Args:
        config: Configuration object
        
    Returns:
        State: initial state with positions, velocities, and species
    """
    # Check if config has custom initialization method
    if hasattr(config, 'get_initial_state'):
        return config.get_initial_state()
    
    # Otherwise use default initialization
    return initialize_state_default(config)


def initialize_state_default(config):
    """
    Default initialization - random positions and velocities.
    
    Args:
        config: Configuration object
        
    Returns:
        State: initial state
    """
    n_agents = config.n_agents
    dimension = config.dimension
    
    # Initialize arrays
    positions = np.zeros((n_agents, dimension))
    velocities = np.zeros((n_agents, dimension))
    species = np.zeros(n_agents, dtype=int)
    
    # Random positions in domain
    positions = np.random.uniform(
        low=0,
        high=config.domain_size,
        size=(n_agents, dimension)
    )
    
    # Get velocity initialization parameters
    if hasattr(config, 'v_init_max'):
        v_init_max = config.v_init_max
    else:
        # Use average of species velocities
        v_init_max = (config.v_max + config.v_max_sp2) / 2
    
    # Random velocities
    velocities = np.random.uniform(
        low=-v_init_max,
        high=v_init_max,
        size=(n_agents, dimension)
    )
    
    # Assign species labels
    species[:config.n_species1] = config.species1_label
    species[config.n_species1:] = config.species2_label
    
    # Normalize velocities to appropriate speeds
    for i in range(n_agents):
        speed = np.linalg.norm(velocities[i])
        if speed > 0:
            if species[i] == config.species1_label:
                target_speed = np.random.uniform(config.v_min, config.v_max)
            else:
                target_speed = np.random.uniform(config.v_min_sp2, config.v_max_sp2)
            velocities[i] = velocities[i] * (target_speed / speed)
    
    return State(positions, velocities, species)


def initialize_clustered(config, cluster_centers=None, cluster_radius=None):
    """
    Initialize boids in clusters.
    
    Args:
        config: Configuration object
        cluster_centers: list of cluster center positions (optional)
        cluster_radius: radius of each cluster (optional)
        
    Returns:
        State: initial state with clustered positions
    """
    n_agents = config.n_agents
    dimension = config.dimension
    
    positions = np.zeros((n_agents, dimension))
    velocities = np.zeros((n_agents, dimension))
    species = np.zeros(n_agents, dtype=int)
    
    # Default cluster parameters
    if cluster_centers is None:
        # Create clusters at random positions
        n_clusters = 2
        cluster_centers = []
        for _ in range(n_clusters):
            center = np.random.uniform(0, config.domain_size, size=dimension)
            cluster_centers.append(center)
    
    if cluster_radius is None:
        cluster_radius = min(config.domain_size) * 0.1
    
    # Assign agents to clusters
    agents_per_cluster = n_agents // len(cluster_centers)
    
    for cluster_idx, center in enumerate(cluster_centers):
        start_idx = cluster_idx * agents_per_cluster
        end_idx = start_idx + agents_per_cluster if cluster_idx < len(cluster_centers) - 1 else n_agents
        
        for i in range(start_idx, end_idx):
            # Random position in sphere/circle around cluster center
            if dimension == 2:
                angle = np.random.uniform(0, 2*np.pi)
                r = cluster_radius * np.sqrt(np.random.uniform(0, 1))
                offset = r * np.array([np.cos(angle), np.sin(angle)])
            else:  # dimension == 3
                theta = np.random.uniform(0, 2*np.pi)
                phi = np.random.uniform(0, np.pi)
                r = cluster_radius * np.cbrt(np.random.uniform(0, 1))
                offset = r * np.array([
                    np.sin(phi) * np.cos(theta),
                    np.sin(phi) * np.sin(theta),
                    np.cos(phi)
                ])
            
            positions[i] = center + offset
            
            # Wrap to domain
            positions[i] = np.mod(positions[i], config.domain_size)
            
            # Assign species
            if i < config.n_species1:
                species[i] = config.species1_label
                target_speed = np.random.uniform(config.v_min, config.v_max)
            else:
                species[i] = config.species2_label
                target_speed = np.random.uniform(config.v_min_sp2, config.v_max_sp2)
            
            # Random velocity direction
            if dimension == 2:
                angle = np.random.uniform(0, 2*np.pi)
                velocities[i] = target_speed * np.array([np.cos(angle), np.sin(angle)])
            else:  # dimension == 3
                direction = np.random.randn(dimension)
                direction = direction / np.linalg.norm(direction)
                velocities[i] = target_speed * direction
    
    return State(positions, velocities, species)


def initialize_grid(config, spacing=None):
    """
    Initialize boids on a regular grid.
    
    Args:
        config: Configuration object
        spacing: grid spacing (optional)
        
    Returns:
        State: initial state with grid positions
    """
    n_agents = config.n_agents
    dimension = config.dimension
    
    if spacing is None:
        # Calculate spacing to fit all agents
        agents_per_dim = int(np.ceil(n_agents ** (1/dimension)))
        spacing = min(config.domain_size) / agents_per_dim
    
    positions = np.zeros((n_agents, dimension))
    velocities = np.zeros((n_agents, dimension))
    species = np.zeros(n_agents, dtype=int)
    
    # Create grid
    if dimension == 2:
        nx = int(np.ceil(np.sqrt(n_agents)))
        ny = nx
        idx = 0
        for i in range(nx):
            for j in range(ny):
                if idx >= n_agents:
                    break
                positions[idx] = [i * spacing, j * spacing]
                idx += 1
    else:  # dimension == 3
        nx = int(np.ceil(n_agents ** (1/3)))
        ny = nx
        nz = nx
        idx = 0
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if idx >= n_agents:
                        break
                    positions[idx] = [i * spacing, j * spacing, k * spacing]
                    idx += 1
    
    # Center grid in domain
    positions += (np.array(config.domain_size) - positions.max(axis=0)) / 2
    
    # Assign species and velocities
    for i in range(n_agents):
        if i < config.n_species1:
            species[i] = config.species1_label
            target_speed = np.random.uniform(config.v_min, config.v_max)
        else:
            species[i] = config.species2_label
            target_speed = np.random.uniform(config.v_min_sp2, config.v_max_sp2)
        
        # Random velocity direction
        if dimension == 2:
            angle = np.random.uniform(0, 2*np.pi)
            velocities[i] = target_speed * np.array([np.cos(angle), np.sin(angle)])
        else:  # dimension == 3
            direction = np.random.randn(dimension)
            direction = direction / np.linalg.norm(direction)
            velocities[i] = target_speed * direction
    
    return State(positions, velocities, species)