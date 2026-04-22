"""
Core package for chase-and-escape simulation
"""

from .agents import Target, Chaser
from .lattice import EMPTY, TARGET, CHASER, create_lattice
from .simulation import Simulation

__all__ = [
    "Target",
    "Chaser",
    "EMPTY",
    "TARGET",
    "CHASER",
    "create_lattice",
    "Simulation",
]