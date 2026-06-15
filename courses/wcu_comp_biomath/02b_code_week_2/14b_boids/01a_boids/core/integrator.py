"""
Time integration for Reynolds boids simulation.
"""
import numpy as np
from .state import State


def integrate_step(state, domain, config, accelerations):
    """
    Perform one time step using Euler integration.
    
    Args:
        state: Current State object
        domain: Domain object
        config: Configuration object
        accelerations: (n_agents, dimension) array of accelerations
        
    Returns:
        State: New state after time step
    """
    dt = config.dt
    
    # Update velocities
    new_velocities = state.velocities + accelerations * dt
    
    # Apply speed limits per species
    for species_label in [config.species1_label, config.species2_label]:
        params = config.get_species_params(species_label)
        mask = state.get_species_mask(species_label)
        
        # Limit speed for this species
        speeds = np.linalg.norm(new_velocities[mask], axis=1)
        over_limit = speeds > params['v_max']
        
        if np.any(over_limit):
            # Normalize and scale to max speed
            indices = np.where(mask)[0][over_limit]
            for i in indices:
                speed = np.linalg.norm(new_velocities[i])
                new_velocities[i] = (new_velocities[i] / speed) * params['v_max']
    
    # Update positions
    new_positions = state.positions + new_velocities * dt
    
    # Apply periodic boundary conditions
    new_positions = domain.wrap(new_positions)
    
    # Create new state
    new_state = State(new_positions, new_velocities, state.species.copy())
    
    return new_state


def integrate_step_rk2(state, domain, config, compute_accel_func):
    """
    Perform one time step using 2nd order Runge-Kutta (midpoint method).
    
    Args:
        state: Current State object
        domain: Domain object
        config: Configuration object
        compute_accel_func: function to compute accelerations
        
    Returns:
        State: New state after time step
    """
    dt = config.dt
    
    # Step 1: Compute accelerations at current state
    accel1 = compute_accel_func(state, domain, config)
    
    # Step 2: Half step
    vel_half = state.velocities + 0.5 * accel1 * dt
    pos_half = state.positions + 0.5 * vel_half * dt
    pos_half = domain.wrap(pos_half)
    
    state_half = State(pos_half, vel_half, state.species.copy())
    
    # Step 3: Compute accelerations at half step
    accel2 = compute_accel_func(state_half, domain, config)
    
    # Step 4: Full step using midpoint acceleration
    new_velocities = state.velocities + accel2 * dt
    
    # Apply speed limits per species
    for species_label in [config.species1_label, config.species2_label]:
        params = config.get_species_params(species_label)
        mask = state.get_species_mask(species_label)
        
        speeds = np.linalg.norm(new_velocities[mask], axis=1)
        over_limit = speeds > params['v_max']
        
        if np.any(over_limit):
            indices = np.where(mask)[0][over_limit]
            for i in indices:
                speed = np.linalg.norm(new_velocities[i])
                new_velocities[i] = (new_velocities[i] / speed) * params['v_max']
    
    # Update positions
    new_positions = state.positions + new_velocities * dt
    new_positions = domain.wrap(new_positions)
    
    # Create new state
    new_state = State(new_positions, new_velocities, state.species.copy())
    
    return new_state