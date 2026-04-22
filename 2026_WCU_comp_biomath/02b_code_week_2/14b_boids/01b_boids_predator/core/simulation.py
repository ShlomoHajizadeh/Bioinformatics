"""
Main simulation class for Reynolds boids.
"""
import numpy as np
from core.state import State
from core.domain import Domain
from core.rules import compute_accelerations
from core.integrator import integrate_step


class Simulation:
    """
    Main simulation class that orchestrates the boids simulation.
    """
    
    def __init__(self, config):
        """
        Initialize simulation.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.state = config.get_initial_state()
        self.domain = Domain(config.domain_size)
        self.current_step = 0
        self.history = []
        
    def step(self):
        """
        Perform one simulation step.
        """
        # Compute accelerations based on boids rules
        accelerations = compute_accelerations(self.state, self.domain, self.config)
        
        # Integrate equations of motion
        self.state = integrate_step(self.state, accelerations, self.domain, self.config)
        
        # Increment step counter
        self.current_step += 1
        
    def run(self):
        """
        Run the full simulation.
        
        Returns:
            list of State objects (history)
        """
        print(f"\nRunning simulation for {self.config.n_steps} steps...")
        
        # Save initial state
        self.history.append(self.state.copy())
        
        # Main simulation loop
        for step in range(self.config.n_steps):
            self.step()
            
            # Save state at specified intervals
            if (step + 1) % self.config.save_every == 0:
                self.history.append(self.state.copy())
                
            # Progress indicator
            if (step + 1) % (self.config.n_steps // 10) == 0:
                progress = 100 * (step + 1) / self.config.n_steps
                print(f"Progress: {progress:.0f}% ({step + 1}/{self.config.n_steps} steps)")
        
        print(f"\nSimulation complete!")
        print(f"Saved {len(self.history)} snapshots")
        
        return self.history
    
    def reset(self):
        """
        Reset simulation to initial state.
        """
        self.state = self.config.get_initial_state()
        self.current_step = 0
        self.history = []