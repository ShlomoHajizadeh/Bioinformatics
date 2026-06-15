"""
Main simulation class for Reynolds boids.
"""
import numpy as np
from .state import State
from .domain import Domain
from .initialization import initialize_state
from .rules import compute_accelerations
from .integrator import integrate_step


class Simulation:
    """
    Reynolds boids simulation manager.
    
    Attributes:
        config: Configuration object
        domain: Domain object
        state: Current State object
        history: List of saved State objects
    """
    
    def __init__(self, config):
        """
        Initialize simulation.
        
        Args:
            config: Configuration object (Config2D or Config3D)
        """
        self.config = config
        self.domain = Domain(config.domain_size)
        self.state = initialize_state(config)
        self.history = []
        self.current_step = 0
        
    def step(self):
        """Perform one simulation step."""
        # Compute accelerations based on Reynolds rules
        accelerations = compute_accelerations(self.state, self.domain, self.config)
        
        # Integrate forward in time
        self.state = integrate_step(self.state, self.domain, self.config, accelerations)
        
        self.current_step += 1
        
    def run(self, n_steps=None):
        """
        Run the simulation for a specified number of steps.
        
        Args:
            n_steps: number of steps to run (uses config.n_steps if None)
            
        Returns:
            list: History of saved states
        """
        if n_steps is None:
            n_steps = self.config.n_steps
        
        # Save initial state
        self.history.append(self.state.copy())
        
        print(f"Running simulation for {n_steps} steps...")
        
        for step in range(n_steps):
            self.step()
            
            # Save state periodically
            if (step + 1) % self.config.save_every == 0:
                self.history.append(self.state.copy())
                
                # Print progress
                if (step + 1) % (self.config.save_every * 10) == 0:
                    progress = 100 * (step + 1) / n_steps
                    print(f"  Progress: {progress:.1f}% (step {step + 1}/{n_steps})")
        
        return self.history
    
    def reset(self):
        """Reset simulation to initial conditions."""
        self.state = initialize_state(self.config)
        self.history = []
        self.current_step = 0
        
    def get_current_state(self):
        """Get the current state."""
        return self.state
    
    def get_history(self):
        """Get the full history of saved states."""
        return self.history