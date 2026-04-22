"""
Configuration for 3D Reynolds boids simulation.
"""


class Config3D:
    """Configuration parameters for 3D simulation."""
    
    def __init__(self):
        # Domain
        self.dimension = 3
        self.domain_size = [100.0, 100.0, 100.0]  # [width, height, depth]
        
        # Species 1: Boids (full rules)
        self.n_species1 = 300  # Large number
        self.species1_label = 0
        
        # Species 2: Avoidance-only agents
        self.n_species2 = 30  # Small number
        self.species2_label = 1
        
        # Total agents
        self.n_agents = self.n_species1 + self.n_species2
        
        # Radii for different behaviors
        self.r_avoidance_sp1 = 5.0      # Avoidance radius for species 1
        self.r_avoidance_sp2 = 3.0      # Smaller avoidance radius for species 2
        self.r_alignment = 15.0          # Alignment radius (species 1 only)
        self.r_cohesion = 15.0           # Cohesion radius (species 1 only)
        
        # Weights for different rules (species 1)
        self.w_avoidance = 1.5
        self.w_alignment = 1.0
        self.w_cohesion = 0.8
        
        # Weight for species 2 avoidance
        self.w_avoidance_sp2 = 2.0
        
        # Speed limits
        self.v_max_sp1 = 2.0   # Maximum speed for species 1
        self.v_max_sp2 = 1.5   # Maximum speed for species 2
        self.v_init_max = 1.0  # Maximum initial speed
        
        # Time integration
        self.dt = 0.1          # Time step
        self.n_steps = 1000    # Total number of steps
        self.save_every = 10   # Save snapshot every N steps
        
        # Random seed
        self.random_seed = 42
        
    def get_species_params(self, species_label):
        """Get parameters for a specific species."""
        if species_label == self.species1_label:
            return {
                'r_avoidance': self.r_avoidance_sp1,
                'r_alignment': self.r_alignment,
                'r_cohesion': self.r_cohesion,
                'w_avoidance': self.w_avoidance,
                'w_alignment': self.w_alignment,
                'w_cohesion': self.w_cohesion,
                'v_max': self.v_max_sp1,
                'full_rules': True
            }
        else:  # species2_label
            return {
                'r_avoidance': self.r_avoidance_sp2,
                'r_alignment': 0.0,
                'r_cohesion': 0.0,
                'w_avoidance': self.w_avoidance_sp2,
                'w_alignment': 0.0,
                'w_cohesion': 0.0,
                'v_max': self.v_max_sp2,
                'full_rules': False
            }