"""Configuration parameters for the Vicsek model."""
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class VicsekConfig:
    """Configuration parameters for Vicsek flocking simulation.
    
    Attributes:
        N: Number of particles
        L: Domain size (L x L toroidal domain)
        r: Interaction radius for neighbor detection
        nu_0: Absolute velocity of all particles
        eta: Noise strength (temperature-like parameter)
        h: Time step size
        n_steps: Number of simulation steps
        seed: Random seed for reproducibility
    """
    N: int = 300
    L: float = 10.0
    r: float = 1.0
    nu_0: float = 0.5
    eta: float = 0.5
    h: float = 1.0
    n_steps: int = 1000
    seed: Optional[int] = 42
    
    def __post_init__(self):
        """Validate parameters."""
        assert self.N > 0, "Number of particles must be positive"
        assert self.L > 0, "Domain size must be positive"
        assert self.r > 0, "Interaction radius must be positive"
        assert self.nu_0 > 0, "Velocity must be positive"
        assert self.eta >= 0, "Noise strength must be non-negative"
        assert self.h > 0, "Time step must be positive"
        assert self.n_steps > 0, "Number of steps must be positive"