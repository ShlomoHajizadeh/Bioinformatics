"""
Analysis package for chase-and-escape simulation
"""

from .observables import count_alive_targets
from .reporter import SimulationReporter

__all__ = [
    "count_alive_targets",
    "SimulationReporter",
]