"""
Global configuration for the chase-and-escape simulation
"""

from dataclasses import dataclass


@dataclass
class Config:
    LX: int = 15
    LY: int = 15

    N_CHASERS: int = 12
    N_TARGETS: int = 20

    N_STEPS: int = 200

    RANDOM_SEED: int = 42

    DEBUG: bool = True
    PLOT_EVERY: int = 1