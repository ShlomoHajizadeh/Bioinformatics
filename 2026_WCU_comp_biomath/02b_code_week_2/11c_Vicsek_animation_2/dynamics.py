"""Vicsek model dynamics: heading and position updates."""
import numpy as np
from config import VicsekConfig
from neighborhood import find_neighbors


def average_heading(headings: np.ndarray, neighbor_indices: np.ndarray) -> float:
    """Compute average heading angle of neighbors.
    
    Uses the circular mean by averaging unit vectors.
    
    Args:
        headings: Array of all particle headings
        neighbor_indices: Indices of neighboring particles
        
    Returns:
        avg_heading: Average heading angle in radians
    """
    neighbor_headings = headings[neighbor_indices]
    
    # Convert to unit vectors and average
    avg_x = np.mean(np.cos(neighbor_headings))
    avg_y = np.mean(np.sin(neighbor_headings))
    
    # Convert back to angle
    avg_heading = np.arctan2(avg_y, avg_x)
    
    return avg_heading


def update_headings(headings: np.ndarray, positions: np.ndarray, 
                   config: VicsekConfig) -> np.ndarray:
    """Update particle headings according to Vicsek dynamics.
    
    θ_i(t_{n+1}) = E(θ_{i,r}(t_n)) + η ξ_n
    
    Args:
        headings: Current headings of shape (N,)
        positions: Current positions of shape (N, 2)
        config: Vicsek configuration parameters
        
    Returns:
        new_headings: Updated headings of shape (N,)
    """
    N = config.N
    eta = config.eta
    
    # Find neighbors for all particles
    neighbors = find_neighbors(positions, config)
    
    # Compute new headings
    new_headings = np.zeros(N)
    
    for i in range(N):
        # Average heading of neighbors
        avg_theta = average_heading(headings, neighbors[i])
        
        # Add noise
        noise = eta * np.random.uniform(-np.pi, np.pi)
        
        new_headings[i] = avg_theta + noise
    
    # Normalize to [-π, π]
    new_headings = np.arctan2(np.sin(new_headings), np.cos(new_headings))
    
    return new_headings


def update_positions(positions: np.ndarray, headings: np.ndarray, 
                    config: VicsekConfig) -> np.ndarray:
    """Update particle positions according to Vicsek dynamics.
    
    x_i(t_{n+1}) = x_i(t_n) + h ν_0 cos(θ_i(t_{n+1}))
    y_i(t_{n+1}) = y_i(t_n) + h ν_0 sin(θ_i(t_{n+1}))
    
    Args:
        positions: Current positions of shape (N, 2)
        headings: Current headings of shape (N,)
        config: Vicsek configuration parameters
        
    Returns:
        new_positions: Updated positions of shape (N, 2) with periodic BC
    """
    h = config.h
    nu_0 = config.nu_0
    L = config.L
    
    # Compute velocity vectors
    velocities = nu_0 * np.column_stack([np.cos(headings), np.sin(headings)])
    
    # Update positions
    new_positions = positions + h * velocities
    
    # Apply periodic boundary conditions
    new_positions = new_positions % L
    
    return new_positions


def step(positions: np.ndarray, headings: np.ndarray, 
         config: VicsekConfig) -> tuple[np.ndarray, np.ndarray]:
    """Perform one time step of Vicsek dynamics.
    
    Args:
        positions: Current positions of shape (N, 2)
        headings: Current headings of shape (N,)
        config: Vicsek configuration parameters
        
    Returns:
        new_positions: Updated positions of shape (N, 2)
        new_headings: Updated headings of shape (N,)
    """
    # Update headings first (based on current positions)
    new_headings = update_headings(headings, positions, config)
    
    # Update positions (based on new headings)
    new_positions = update_positions(positions, new_headings, config)
    
    return new_positions, new_headings