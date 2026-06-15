"""
Runs the simulation loop.
"""
import numpy as np
from model.integrator import rk4_step
from simulation.diagnostics import compute_diagnostics

def run_simulation(state, dt, T_total, F, L, G, U):
    """
    Run the swarm simulation.
    
    Parameters:
    -----------
    state : SwarmState
        Initial state
    dt : float
        Time step
    T_total : float
        Total simulation time
    F, L, G, U : float
        Model parameters
    
    Returns:
    --------
    dict
        Dictionary containing:
        - 'history_positions': list of position arrays
        - 'history_grounded': list of grounded masks
        - 'times': array of time points
        - 'diagnostics': dictionary of diagnostic time series
    """
    n_steps = int(T_total / dt)
    times = np.linspace(0, T_total, n_steps + 1)
    
    history_positions = [state.positions.copy()]
    history_grounded = [state.grounded.copy()]
    
    diagnostics = {
        'mean_height': [],
        'grounded_count': [],
        'center_x': [],
        'center_z': [],
        'width': [],
        'height': []
    }
    
    # Compute initial diagnostics
    diag = compute_diagnostics(state)
    for key in diagnostics:
        diagnostics[key].append(diag[key])
    
    # Time stepping
    for step in range(n_steps):
        # RK4 integration step
        new_positions = rk4_step(state, dt, F, L, G, U)
        state.update_positions(new_positions)
        
        # Store history
        history_positions.append(state.positions.copy())
        history_grounded.append(state.grounded.copy())
        
        # Compute diagnostics
        diag = compute_diagnostics(state)
        for key in diagnostics:
            diagnostics[key].append(diag[key])
    
    return {
        'history_positions': history_positions,
        'history_grounded': history_grounded,
        'times': times,
        'diagnostics': diagnostics
    }