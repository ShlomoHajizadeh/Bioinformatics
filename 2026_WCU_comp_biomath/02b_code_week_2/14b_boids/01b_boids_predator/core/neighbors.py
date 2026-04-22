"""
Neighbor finding algorithms for Reynolds boids simulation.
"""
import numpy as np


def find_neighbors_naive(positions, domain, radius):
    """
    Find neighbors within radius using naive O(N^2) algorithm.
    
    Args:
        positions: (n_agents, dimension) array of positions
        domain: Domain object for periodic boundaries
        radius: interaction radius
        
    Returns:
        list: list of neighbor indices for each agent
    """
    n_agents = len(positions)
    neighbors = [[] for _ in range(n_agents)]
    
    for i in range(n_agents):
        for j in range(n_agents):
            if i != j:
                # Compute distance with periodic boundaries
                diff = positions[j] - positions[i]
                diff = domain.minimum_image(diff)
                distance = np.linalg.norm(diff)
                
                if distance < radius:
                    neighbors[i].append(j)
    
    return neighbors


def find_neighbors_efficient(positions, domain, radius, species_filter=None):
    """
    Find neighbors within radius using vectorized operations.
    
    Args:
        positions: (n_agents, dimension) array of positions
        domain: Domain object for periodic boundaries
        radius: interaction radius
        species_filter: optional boolean mask to filter which agents to consider as neighbors
        
    Returns:
        list: list of neighbor indices for each agent
    """
    n_agents = len(positions)
    neighbors = [[] for _ in range(n_agents)]
    
    # If species filter provided, get indices of filtered agents
    if species_filter is not None:
        filtered_indices = np.where(species_filter)[0]
    else:
        filtered_indices = np.arange(n_agents)
    
    # For each agent
    for i in range(n_agents):
        # Compute vectors to all potential neighbors
        diff = positions[filtered_indices] - positions[i]
        
        # Apply minimum image convention
        diff = domain.minimum_image(diff)
        
        # Compute distances
        distances = np.linalg.norm(diff, axis=1)
        
        # Find neighbors within radius (excluding self if in filtered set)
        if species_filter is None:
            # Exclude self
            neighbor_mask = (distances < radius) & (distances > 0)
            neighbor_indices = filtered_indices[neighbor_mask]
        else:
            # Only include filtered agents
            neighbor_mask = (distances < radius)
            neighbor_indices = filtered_indices[neighbor_mask]
        
        neighbors[i] = neighbor_indices.tolist()
    
    return neighbors


def find_neighbors_cell_list(positions, domain, radius, cell_size=None):
    """
    Find neighbors using cell list algorithm for better performance.
    
    Args:
        positions: (n_agents, dimension) array of positions
        domain: Domain object
        radius: interaction radius
        cell_size: size of cells (default: radius)
        
    Returns:
        list: list of neighbor indices for each agent
    """
    n_agents, dimension = positions.shape
    
    if cell_size is None:
        cell_size = radius
    
    # Number of cells in each dimension
    n_cells = np.ceil(np.array(domain.size) / cell_size).astype(int)
    
    # Create cell list
    cells = {}
    agent_to_cell = np.zeros(n_agents, dtype=int)
    
    # Assign agents to cells
    for i in range(n_agents):
        cell_idx = tuple((positions[i] / cell_size).astype(int) % n_cells)
        
        if cell_idx not in cells:
            cells[cell_idx] = []
        cells[cell_idx].append(i)
        
        # Store cell index for each agent (flattened)
        agent_to_cell[i] = np.ravel_multi_index(cell_idx, n_cells)
    
    # Find neighbors
    neighbors = [[] for _ in range(n_agents)]
    
    for i in range(n_agents):
        # Get cell of agent i
        cell_idx = np.unravel_index(agent_to_cell[i], n_cells)
        
        # Check neighboring cells
        for offset in get_neighbor_cells(dimension):
            neighbor_cell = tuple((np.array(cell_idx) + offset) % n_cells)
            
            if neighbor_cell in cells:
                for j in cells[neighbor_cell]:
                    if i != j:
                        # Check distance
                        diff = positions[j] - positions[i]
                        diff = domain.minimum_image(diff)
                        distance = np.linalg.norm(diff)
                        
                        if distance < radius:
                            neighbors[i].append(j)
    
    return neighbors


def get_neighbor_cells(dimension):
    """
    Get offsets for neighboring cells in cell list algorithm.
    
    Args:
        dimension: spatial dimension (2 or 3)
        
    Returns:
        list: list of offset tuples
    """
    if dimension == 2:
        # 3x3 grid of cells
        offsets = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                offsets.append((i, j))
        return offsets
    elif dimension == 3:
        # 3x3x3 grid of cells
        offsets = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    offsets.append((i, j, k))
        return offsets
    else:
        raise ValueError(f"Dimension {dimension} not supported")


def find_neighbors_kdtree(positions, domain, radius):
    """
    Find neighbors using KD-tree (requires scipy).
    Note: This doesn't handle periodic boundaries correctly.
    
    Args:
        positions: (n_agents, dimension) array of positions
        domain: Domain object
        radius: interaction radius
        
    Returns:
        list: list of neighbor indices for each agent
    """
    try:
        from scipy.spatial import KDTree
    except ImportError:
        print("Warning: scipy not available, falling back to efficient method")
        return find_neighbors_efficient(positions, domain, radius)
    
    # Build KD-tree
    tree = KDTree(positions)
    
    # Query neighbors
    neighbors_list = tree.query_ball_tree(tree, radius)
    
    # Remove self from neighbor lists
    neighbors = []
    for i, neighbor_list in enumerate(neighbors_list):
        neighbors.append([j for j in neighbor_list if j != i])
    
    return neighbors


def compute_distance_matrix(positions, domain):
    """
    Compute pairwise distance matrix with periodic boundaries.
    
    Args:
        positions: (n_agents, dimension) array of positions
        domain: Domain object
        
    Returns:
        ndarray: (n_agents, n_agents) distance matrix
    """
    n_agents = len(positions)
    distances = np.zeros((n_agents, n_agents))
    
    for i in range(n_agents):
        diff = positions - positions[i]
        diff = domain.minimum_image(diff)
        distances[i] = np.linalg.norm(diff, axis=1)
    
    return distances


def find_k_nearest_neighbors(positions, domain, k):
    """
    Find k nearest neighbors for each agent.
    
    Args:
        positions: (n_agents, dimension) array of positions
        domain: Domain object
        k: number of nearest neighbors
        
    Returns:
        list: list of k nearest neighbor indices for each agent
    """
    n_agents = len(positions)
    neighbors = [[] for _ in range(n_agents)]
    
    # Compute distance matrix
    distances = compute_distance_matrix(positions, domain)
    
    # For each agent, find k nearest (excluding self)
    for i in range(n_agents):
        # Set self-distance to infinity to exclude it
        distances[i, i] = np.inf
        
        # Get indices of k smallest distances
        nearest_indices = np.argpartition(distances[i], k)[:k]
        neighbors[i] = nearest_indices.tolist()
    
    return neighbors


def count_neighbors_in_radius(positions, domain, radius):
    """
    Count number of neighbors within radius for each agent.
    
    Args:
        positions: (n_agents, dimension) array of positions
        domain: Domain object
        radius: interaction radius
        
    Returns:
        ndarray: (n_agents,) array of neighbor counts
    """
    neighbors = find_neighbors_efficient(positions, domain, radius)
    return np.array([len(n) for n in neighbors])