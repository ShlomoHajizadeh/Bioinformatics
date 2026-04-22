"""
Configuration for 3D predator-prey simulation.
"""
import numpy as np
from core.state import State


class Config3DPredatorPrey:
    """Configuration for 3D fish school avoiding sharks."""
    
    def __init__(self):
        # Domain
        self.dimension = 3
        self.domain_size = (20, 20, 20)  # Smaller domain
        
        # Agents
        self.n_species1 = 800  # Prey (fish)
        self.n_species2 = 2    # Predators (sharks)
        self.n_agents = self.n_species1 + self.n_species2
        
        # Species labels
        self.species1_label = 1  # Prey
        self.species2_label = 2  # Predators
        
        # Time parameters
        self.dt = 0.05  # Smaller timestep
        self.n_steps = 100
        self.save_every = 10
        
        # Species 1 (Prey) parameters
        self.v_min = 1.5
        self.v_max = 2.5
        
        # Species 2 (Predator) parameters
        self.v_min_sp2 = 0.5
        self.v_max_sp2 = 1.2
        
        # Interaction radii for prey (species 1)
        self.r_avoid = 3.0
        self.r_align = 8.0
        self.r_cohesion = 10.0
        
        # Interaction radii for predators (species 2)
        self.r_avoid_sp2 = 15.0
        
        # Inter-species interaction
        self.r_avoid_interspecies = 25.0
        
        # Rule weights for prey (species 1)
        self.w_avoid = 5.0
        self.w_align = 8.0
        self.w_cohesion = 0.05  # Reduced to avoid clumping
        self.w_avoidance_interspecies = 5.0
        
        # Rule weights for predators (species 2)
        self.w_avoid_sp2 = 1.0
        self.w_hunt = 2.0
    
    def get_initial_state(self):
        """Generate initial state with two species."""
        # Initialize prey (species 1)
        positions_sp1 = np.random.rand(self.n_species1, self.dimension) * self.domain_size
        velocities_sp1 = np.random.randn(self.n_species1, self.dimension)
        velocities_sp1 = velocities_sp1 / np.linalg.norm(velocities_sp1, axis=1, keepdims=True)
        velocities_sp1 *= np.random.uniform(self.v_min, self.v_max, (self.n_species1, 1))
        species_sp1 = np.full(self.n_species1, self.species1_label, dtype=int)
        
        # Initialize predators (species 2) - start at edges
        positions_sp2 = np.zeros((self.n_species2, self.dimension))
        for i in range(self.n_species2):
            if i == 0:
                positions_sp2[i] = [5, self.domain_size[1] / 2, self.domain_size[2] / 2]
            elif i == 1:
                positions_sp2[i] = [self.domain_size[0] - 5, self.domain_size[1] / 2, self.domain_size[2] / 2]
            elif i == 2:
                positions_sp2[i] = [self.domain_size[0] / 2, 5, self.domain_size[2] / 2]
            elif i == 3:
                positions_sp2[i] = [self.domain_size[0] / 2, self.domain_size[1] - 5, self.domain_size[2] / 2]
            elif i == 4:
                positions_sp2[i] = [self.domain_size[0] / 2, self.domain_size[1] / 2, 5]
            else:
                positions_sp2[i] = [self.domain_size[0] / 2, self.domain_size[1] / 2, self.domain_size[2] - 5]
        
        velocities_sp2 = np.random.randn(self.n_species2, self.dimension)
        velocities_sp2 = velocities_sp2 / np.linalg.norm(velocities_sp2, axis=1, keepdims=True)
        velocities_sp2 *= np.random.uniform(self.v_min_sp2, self.v_max_sp2, (self.n_species2, 1))
        species_sp2 = np.full(self.n_species2, self.species2_label, dtype=int)
        
        # Combine
        positions = np.vstack([positions_sp1, positions_sp2])
        velocities = np.vstack([velocities_sp1, velocities_sp2])
        species = np.hstack([species_sp1, species_sp2])
        
        return State(positions, velocities, species)