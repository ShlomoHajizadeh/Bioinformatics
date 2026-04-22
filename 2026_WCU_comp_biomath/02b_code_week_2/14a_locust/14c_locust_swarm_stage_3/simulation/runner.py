"""
Runs the simulation time-stepping loop.
"""
import numpy as np
from model.forces import compute_total_force
from model.boundary import apply_boundary_conditions
from simulation.diagnostics import compute_diagnostics, compute_rolling_diagnostics

def euler_step(state, dt, F, L, G, U):
    """
    Perform one Euler time step.
    
    Parameters:
    -----------
    state : SwarmState
        Current state
    dt : float
        Time step
    F, L, G, U : float
        Force parameters
    
    Returns:
    --------
    ndarray
        Velocities after this step (for diagnostics)
    """
    # Compute forces
    forces = compute_total_force(state, F, L, G, U)
    
    # Compute velocities (v = F, using unit mass)
    velocities = forces
    
    # Apply boundary conditions to velocities BEFORE updating positions
    velocities = apply_boundary_conditions(state, velocities)
    
    # Update positions
    state.positions += velocities * dt
    
    # SAFETY CHECK: Enforce ground boundary after position update
    # This prevents numerical drift below ground
    for i in range(state.N):
        if state.positions[i, 1] < 0:
            state.positions[i, 1] = 0
            state.grounded[i] = True
    
    return velocities

def run_simulation(state, dt, T_total, F, L, G, U):
    """
    Run the full simulation.
    
    Parameters:
    -----------
    state : SwarmState
        Initial state
    dt : float
        Time step
    T_total : float
        Total simulation time
    F, L, G, U : float
        Force parameters
    
    Returns:
    --------
    dict
        Results including history and diagnostics
    """
    n_steps = int(T_total / dt)
    
    # Storage for history
    history_positions = []
    history_grounded = []
    times = []
    
    # Storage for diagnostics
    diagnostics = {
        'center_x': [],
        'center_z': [],
        'width': [],
        'height': [],
        'mean_height': [],
        'mean_height_airborne': [],
        'grounded_count': [],
        'airborne_count': [],
        'std_x': [],
        'std_z': [],
        # Rolling diagnostics (Stage 3)
        'mean_rolling_speed': [],
        'rolling_count': [],
        'mean_horizontal_velocity': [],
        'front_position': [],
        'rear_position': [],
        'swarm_length': [],
    }
    
    # Run simulation
    for step in range(n_steps + 1):
        t = step * dt
        
        # SAFETY CHECK: Enforce ground before storing
        for i in range(state.N):
            if state.positions[i, 1] < 0:
                state.positions[i, 1] = 0
                state.grounded[i] = True
        
        # Store current state
        history_positions.append(state.positions.copy())
        history_grounded.append(state.grounded.copy())
        times.append(t)
        
        # Compute and store diagnostics
        diag = compute_diagnostics(state)
        
        # Compute velocities for rolling diagnostics
        if step < n_steps:
            forces = compute_total_force(state, F, L, G, U)
            velocities = forces
            velocities = apply_boundary_conditions(state, velocities)
            
            rolling_diag = compute_rolling_diagnostics(state, velocities)
        else:
            # Last step, use zeros for velocities
            rolling_diag = compute_rolling_diagnostics(state, np.zeros((state.N, 2)))
        
        # Combine diagnostics
        all_diag = {**diag, **rolling_diag}
        
        for key, value in all_diag.items():
            diagnostics[key].append(value)
        
        # Perform time step
        if step < n_steps:
            euler_step(state, dt, F, L, G, U)
        
        # Progress indicator
        if step % 500 == 0:
            print(".", end='', flush=True)
    
    results = {
        'history_positions': history_positions,
        'history_grounded': history_grounded,
        'times': np.array(times),
        'diagnostics': diagnostics,
    }
    
    return results