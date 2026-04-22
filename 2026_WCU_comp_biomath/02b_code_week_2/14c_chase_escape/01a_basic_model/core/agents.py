"""
Agent definitions
"""

from dataclasses import dataclass


@dataclass
class Target:
    id: int
    x: int
    y: int
    alive: bool = True


@dataclass
class Chaser:
    id: int
    x: int
    y: int