"""
Time integration for boids simulation.
"""
import numpy as np
from core.state import State
from core.rules import apply_velocity_limits


def integrate_step(state, accelerations, domain, config):
    """
    Integrate one time step using velocity Verlet algorithm.
    
    Args:
        state: current State
        accelerations: array of acceleration vectors
        domain: Domain object
        config: Configuration object
        
    Returns:
        new State
    """
    dt = config.dt
    
    # Update velocities (half step)
    new_velocities = state.velocities + 0.5 * dt * accelerations
    
    # Apply velocity limits
    new_velocities = apply_velocity_limits(new_velocities, state.species, config)
    
    # Update positions
    new_positions = state.positions + dt * new_velocities
    
    # Apply periodic boundary conditions
    new_positions = domain.wrap(new_positions)
    
    # Update velocities (second half step)
    # Note: In practice, we would compute new accelerations here,
    # but for simplicity we use the same accelerations
    new_velocities = new_velocities + 0.5 * dt * accelerations
    
    # Apply velocity limits again
    new_velocities = apply_velocity_limits(new_velocities, state.species, config)
    
    return State(new_positions, new_velocities, state.species.copy())


def integrate_euler(state, accelerations, domain, config):
    """
    Integrate one time step using simple Euler method.
    
    Args:
        state: current State
        accelerations: array of acceleration vectors
        domain: Domain object
        config: Configuration object
        
    Returns:
        new State
    """
    dt = config.dt
    
    # Update velocities
    new_velocities = state.velocities + dt * accelerations
    
    # Apply velocity limits
    new_velocities = apply_velocity_limits(new_velocities, state.species, config)
    
    # Update positions
    new_positions = state.positions + dt * new_velocities
    
    # Apply periodic boundary conditions
    new_positions = domain.wrap(new_positions)
    
    return State(new_positions, new_velocities, state.species.copy())