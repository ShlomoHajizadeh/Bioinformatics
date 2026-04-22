"""Obstacle avoidance for Vicsek model."""
import numpy as np
from config import VicsekConfig


def distance_to_obstacle(position: np.ndarray, obstacle_center: tuple[float, float]) -> float:
    """Calculate Euclidean distance from position to obstacle center.
    
    Args:
        position: Particle position (x, y)
        obstacle_center: Obstacle center (x, y)
        
    Returns:
        distance: Euclidean distance to obstacle center
    """
    dx = position[0] - obstacle_center[0]
    dy = position[1] - obstacle_center[1]
    return np.sqrt(dx**2 + dy**2)


def angle_to_obstacle(position: np.ndarray, obstacle_center: tuple[float, float]) -> float:
    """Calculate angle from position to obstacle center.
    
    Args:
        position: Particle position (x, y)
        obstacle_center: Obstacle center (x, y)
        
    Returns:
        angle: Angle in radians from position to obstacle
    """
    dx = obstacle_center[0] - position[0]
    dy = obstacle_center[1] - position[1]
    return np.arctan2(dy, dx)


def check_obstacle_interaction(positions: np.ndarray, config: VicsekConfig) -> np.ndarray:
    """Check which particles are within interaction radius of obstacle.
    
    Args:
        positions: Particle positions of shape (N, 2)
        config: Vicsek configuration
        
    Returns:
        interacting: Boolean array of shape (N,) indicating obstacle interaction
    """
    if config.obstacle_center is None:
        return np.zeros(len(positions), dtype=bool)
    
    N = len(positions)
    interacting = np.zeros(N, dtype=bool)
    
    for i in range(N):
        dist = distance_to_obstacle(positions[i], config.obstacle_center)
        # Particle interacts if within radius r of obstacle surface
        if dist <= (config.obstacle_radius + config.r):
            interacting[i] = True
    
    return interacting


def compute_avoidance_heading(position: np.ndarray, current_heading: float, 
                              obstacle_center: tuple[float, float]) -> float:
    """Compute avoidance heading when near obstacle.
    
    Strategy: Turn perpendicular (±90°) to the direction toward obstacle.
    This creates a tangential avoidance maneuver.
    
    Args:
        position: Particle position (x, y)
        current_heading: Current heading angle
        obstacle_center: Obstacle center (x, y)
        
    Returns:
        avoidance_heading: New heading to avoid obstacle
    """
    # Angle from particle to obstacle
    angle_to_obs = angle_to_obstacle(position, obstacle_center)
    
    # Turn perpendicular: add or subtract π/2 with equal probability
    if np.random.rand() < 0.5:
        avoidance_heading = angle_to_obs + np.pi / 2
    else:
        avoidance_heading = angle_to_obs - np.pi / 2
    
    # Normalize to [-π, π]
    avoidance_heading = np.arctan2(np.sin(avoidance_heading), np.cos(avoidance_heading))
    
    return avoidance_heading


def apply_obstacle_avoidance(headings: np.ndarray, positions: np.ndarray, 
                            config: VicsekConfig) -> np.ndarray:
    """Apply obstacle avoidance to particle headings.
    
    Args:
        headings: Current headings of shape (N,)
        positions: Current positions of shape (N, 2)
        config: Vicsek configuration
        
    Returns:
        modified_headings: Headings with obstacle avoidance applied
    """
    if config.obstacle_center is None:
        return headings.copy()
    
    modified_headings = headings.copy()
    interacting = check_obstacle_interaction(positions, config)
    
    for i in range(len(headings)):
        if interacting[i]:
            modified_headings[i] = compute_avoidance_heading(
                positions[i], headings[i], config.obstacle_center
            )
    
    return modified_headings