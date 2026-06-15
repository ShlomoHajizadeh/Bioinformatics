"""
State representation for the boids simulation.
"""
import numpy as np


class State:
    """
    Encapsulates the state of all agents in the simulation.
    
    Attributes:
        positions: (n_agents, dimension) array of positions
        velocities: (n_agents, dimension) array of velocities
        species: (n_agents,) array of species labels
        n_agents: total number of agents
        dimension: spatial dimension (2 or 3)
    """
    
    def __init__(self, positions, velocities, species):
        """
        Initialize state.
        
        Args:
            positions: (n_agents, dimension) array
            velocities: (n_agents, dimension) array
            species: (n_agents,) array of integer labels
        """
        self.positions = np.array(positions, dtype=np.float64)
        self.velocities = np.array(velocities, dtype=np.float64)
        self.species = np.array(species, dtype=np.int32)
        
        self.n_agents = self.positions.shape[0]
        self.dimension = self.positions.shape[1]
        
        # Validate shapes
        assert self.velocities.shape == (self.n_agents, self.dimension)
        assert self.species.shape == (self.n_agents,)
        
    def copy(self):
        """Create a deep copy of the state."""
        return State(
            self.positions.copy(),
            self.velocities.copy(),
            self.species.copy()
        )
    
    def get_species_mask(self, species_label):
        """Get boolean mask for agents of a given species."""
        return self.species == species_label
    
    def get_species_indices(self, species_label):
        """Get indices of agents of a given species."""
        return np.where(self.species == species_label)[0]