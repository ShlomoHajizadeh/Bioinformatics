"""State initialization for the Vicsek model."""
import numpy as np
from config import VicsekConfig


def is_inside_obstacle(position: np.ndarray, obstacle_center: tuple[float, float], 
                       obstacle_radius: float, safety_margin: float = 0.0) -> bool:
    """Check if a position is inside the obstacle (with optional safety margin).
    
    Args:
        position: Position (x, y)
        obstacle_center: Obstacle center (x, y)
        obstacle_radius: Obstacle radius
        safety_margin: Additional margin around obstacle
        
    Returns:
        inside: True if position is inside obstacle (including safety margin)
    """
    dx = position[0] - obstacle_center[0]
    dy = position[1] - obstacle_center[1]
    distance = np.sqrt(dx**2 + dy**2)
    return distance < (obstacle_radius + safety_margin)


def initialize_positions(config: VicsekConfig) -> np.ndarray:
    """Initialize particle positions randomly in the domain.
    
    Ensures particles are not placed inside the obstacle (if present).
    Includes a safety margin of r/2 around the obstacle.
    
    Args:
        config: Vicsek configuration parameters
        
    Returns:
        positions: Array of shape (N, 2) with random positions in [0, L)^2
    """
    positions = np.zeros((config.N, 2))
    
    if config.obstacle_center is None:
        # No obstacle - simple uniform initialization
        positions = np.random.uniform(0, config.L, size=(config.N, 2))
    else:
        # With obstacle - rejection sampling with safety margin
        safety_margin = config.r / 2  # Half the interaction radius
        
        for i in range(config.N):
            valid = False
            attempts = 0
            max_attempts = 1000
            
            while not valid and attempts < max_attempts:
                # Generate random position
                pos = np.random.uniform(0, config.L, size=2)
                
                # Check if outside obstacle (including safety margin)
                if not is_inside_obstacle(pos, config.obstacle_center, 
                                         config.obstacle_radius, safety_margin):
                    positions[i] = pos
                    valid = True
                
                attempts += 1
            
            if attempts >= max_attempts:
                raise RuntimeError(
                    f"Could not find valid position for particle {i} after {max_attempts} attempts. "
                    f"Obstacle (radius={config.obstacle_radius:.2f} + safety margin={safety_margin:.2f}) "
                    f"may be too large for domain size L={config.L:.2f}."
                )
    
    return positions


def initialize_headings(config: VicsekConfig) -> np.ndarray:
    """Initialize particle headings randomly.
    
    Args:
        config: Vicsek configuration parameters
        
    Returns:
        headings: Array of shape (N,) with random headings in [-π, π)
    """
    headings = np.random.uniform(-np.pi, np.pi, size=config.N)
    return headings


def initialize_state(config: VicsekConfig) -> tuple[np.ndarray, np.ndarray]:
    """Initialize the complete state of the Vicsek model.
    
    Args:
        config: Vicsek configuration parameters
        
    Returns:
        positions: Array of shape (N, 2) with particle positions
        headings: Array of shape (N,) with particle headings
    """
    # Set random seed if specified
    if config.seed is not None:
        np.random.seed(config.seed)
    
    # Initialize positions and headings
    positions = initialize_positions(config)
    headings = initialize_headings(config)
    
    return positions, headings