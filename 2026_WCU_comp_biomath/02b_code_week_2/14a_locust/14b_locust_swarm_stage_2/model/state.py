"""
Defines the swarm state and helper functions.
"""
import numpy as np

class SwarmState:
    """
    Represents the state of the locust swarm.
    """
    def __init__(self, N):
        """
        Initialize swarm state.
        
        Parameters:
        -----------
        N : int
            Number of locusts
        """
        self.N = N
        self.positions = np.zeros((N, 2))      # Shape (N, 2): [x, z]
        self.velocities = np.zeros((N, 2))     # Shape (N, 2): [vx, vz]
        self.grounded = np.zeros(N, dtype=bool) # Shape (N,): boolean mask
    
    def copy(self):
        """
        Create a deep copy of the current state.
        
        Returns:
        --------
        SwarmState
            A copy of the current state
        """
        new_state = SwarmState(self.N)
        new_state.positions = self.positions.copy()
        new_state.velocities = self.velocities.copy()
        new_state.grounded = self.grounded.copy()
        return new_state
    
    def update_positions(self, new_positions):
        """
        Update positions.
        
        Parameters:
        -----------
        new_positions : ndarray
            New positions array of shape (N, 2)
        """
        self.positions = new_positions.copy()
    
    def update_velocities(self, new_velocities):
        """
        Update velocities.
        
        Parameters:
        -----------
        new_velocities : ndarray
            New velocities array of shape (N, 2)
        """
        self.velocities = new_velocities.copy()