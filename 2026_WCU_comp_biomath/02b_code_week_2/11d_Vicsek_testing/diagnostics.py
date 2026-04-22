"""Diagnostic functions for Vicsek model analysis."""
import numpy as np
from config import VicsekConfig


def order_parameter(headings: np.ndarray) -> float:
    """Compute order parameter (to be defined later).
    
    Placeholder implementation.
    
    Args:
        headings: Array of particle headings of shape (N,)
        
    Returns:
        order: Order parameter value
    """
    # Placeholder - will be defined later
    # Typical definition: magnitude of average velocity vector
    N = len(headings)
    vx = np.mean(np.cos(headings))
    vy = np.mean(np.sin(headings))
    order = np.sqrt(vx**2 + vy**2)
    return order


def compute_velocities(headings: np.ndarray, nu_0: float) -> np.ndarray:
    """Compute velocity vectors from headings.
    
    Args:
        headings: Array of particle headings of shape (N,)
        nu_0: Absolute velocity
        
    Returns:
        velocities: Array of shape (N, 2) with velocity vectors
    """
    velocities = nu_0 * np.column_stack([np.cos(headings), np.sin(headings)])
    return velocities


def center_of_mass(positions: np.ndarray, L: float) -> np.ndarray:
    """Compute center of mass with periodic boundary conditions.
    
    Args:
        positions: Array of shape (N, 2) with particle positions
        L: Domain size
        
    Returns:
        com: Center of mass coordinates of shape (2,)
    """
    # Convert to angles on unit circle for periodic mean
    theta_x = 2 * np.pi * positions[:, 0] / L
    theta_y = 2 * np.pi * positions[:, 1] / L
    
    com_x = L * np.arctan2(np.mean(np.sin(theta_x)), np.mean(np.cos(theta_x))) / (2 * np.pi)
    com_y = L * np.arctan2(np.mean(np.sin(theta_y)), np.mean(np.cos(theta_y))) / (2 * np.pi)
    
    com = np.array([com_x % L, com_y % L])
    return com


def summary_statistics(positions: np.ndarray, headings: np.ndarray, 
                       config: VicsekConfig) -> dict:
    """Compute summary statistics of the current state.
    
    Args:
        positions: Array of shape (N, 2) with particle positions
        headings: Array of shape (N,) with particle headings
        config: Vicsek configuration parameters
        
    Returns:
        stats: Dictionary with summary statistics
    """
    stats = {
        'order_parameter': order_parameter(headings),
        'center_of_mass': center_of_mass(positions, config.L),
        'mean_heading': np.arctan2(np.mean(np.sin(headings)), np.mean(np.cos(headings))),
        'heading_std': np.std(headings),
    }
    
    return stats