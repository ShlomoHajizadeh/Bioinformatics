"""
Computes forces acting on locusts.
Stage 3: Add wind force with correct social interaction from paper.
"""
import numpy as np

def social_force(state, F, L):
    """
    Compute social interaction forces between locusts.
    
    Uses the CORRECT formula from the paper:
    f_ij = [F * exp(-r_ij / L) - exp(-r_ij)] * r_hat_ij
    
    where r_hat_ij is the unit vector pointing from j to i.
    
    This includes:
    - Long-range attraction: F * exp(-r / L) when F < 1
    - Short-range repulsion: -exp(-r)
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    F : float
        Attraction strength (F < 1 for net attraction at long range)
    L : float
        Length scale of attraction
    
    Returns:
    --------
    ndarray
        Forces on each locust, shape (N, 2)
    """
    N = state.N
    positions = state.positions
    forces = np.zeros((N, 2))
    
    for i in range(N):
        for j in range(N):
            if i != j:
                # Vector from j to i
                r_vec = positions[i] - positions[j]
                r_dist = np.linalg.norm(r_vec)
                
                if r_dist > 1e-10:  # Avoid division by zero
                    # Unit vector from j to i
                    r_hat = r_vec / r_dist
                    
                    # Social force from paper:
                    # f_ij = [F * exp(-r / L) - exp(-r)] * r_hat
                    f_mag = F * np.exp(-r_dist / L) - np.exp(-r_dist)
                    
                    forces[i] += f_mag * r_hat
    
    return forces

def gravity_force(state, G):
    """
    Compute gravitational force (downward).
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    G : float
        Gravity strength
    
    Returns:
    --------
    ndarray
        Gravitational forces, shape (N, 2)
    """
    N = state.N
    forces = np.zeros((N, 2))
    
    # Gravity acts downward (negative z-direction)
    forces[:, 1] = -G
    
    return forces

def wind_force(state, U):
    """
    Compute wind force (horizontal).
    
    Stage 3: Wind pushes locusts horizontally.
    - Airborne locusts: experience full wind force
    - Grounded locusts: experience reduced wind (friction with ground)
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    U : float
        Wind speed (horizontal)
    
    Returns:
    --------
    ndarray
        Wind forces, shape (N, 2)
    """
    N = state.N
    forces = np.zeros((N, 2))
    
    # Wind acts in positive x-direction
    for i in range(N):
        if state.grounded[i]:
            # Grounded locusts experience reduced wind (rolling friction)
            forces[i, 0] = 0.3 * U  # 30% of wind force for grounded
        else:
            # Airborne locusts experience full wind
            forces[i, 0] = U
    
    return forces

def compute_total_force(state, F, L, G, U):
    """
    Compute total force on each locust.
    
    Parameters:
    -----------
    state : SwarmState
        Current swarm state
    F : float
        Social attraction strength (F < 1)
    L : float
        Social interaction length scale (L > 1)
    G : float
        Gravity strength
    U : float
        Wind speed
    
    Returns:
    --------
    ndarray
        Total forces, shape (N, 2)
    """
    f_social = social_force(state, F, L)
    f_gravity = gravity_force(state, G)
    f_wind = wind_force(state, U)
    
    return f_social + f_gravity + f_wind