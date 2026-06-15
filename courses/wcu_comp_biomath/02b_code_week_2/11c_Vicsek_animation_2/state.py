"""State initialization for the Vicsek model."""
import numpy as np
from config import VicsekConfig


def initialize_positions(config: VicsekConfig) -> np.ndarray:
    """Initialize random positions uniformly in [0, L] x [0, L].
    
    Args:
        config: Vicsek configuration parameters
        
    Returns:
        positions: Array of shape (N, 2) with (x, y) coordinates
    """
    if config.seed is not None:
        np.random.seed(config.seed)
    
    positions = np.random.uniform(0, config.L, size=(config.N, 2))
    return positions


def initialize_headings(config: VicsekConfig) -> np.ndarray:
    """Initialize random heading angles uniformly in [-π, π].
    
    Args:
        config: Vicsek configuration parameters
        
    Returns:
        headings: Array of shape (N,) with angles in radians
    """
    if config.seed is not None:
        np.random.seed(config.seed)
    
    headings = np.random.uniform(-np.pi, np.pi, size=config.N)
    return headings


def initialize_state(config: VicsekConfig) -> tuple[np.ndarray, np.ndarray]:
    """Initialize complete system state.
    
    Args:
        config: Vicsek configuration parameters
        
    Returns:
        positions: Array of shape (N, 2) with (x, y) coordinates
        headings: Array of shape (N,) with angles in radians
    """
    if config.seed is not None:
        np.random.seed(config.seed)
    
    positions = initialize_positions(config)
    headings = initialize_headings(config)
    
    return positions, headings