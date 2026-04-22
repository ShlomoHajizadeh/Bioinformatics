"""
Grid initialization utilities.
"""

import numpy as np


def initialize_plant_health(height, width, initial_health):
    """
    Create the plant health array.
    """
    return np.full((height, width), initial_health, dtype=float)


def initialize_egg_queues(height, width, hatch_delay):
    """
    Egg queues:
    eggs[k, i, j] = number of eggs on cell (i,j) that will hatch in k steps.
    """
    return np.zeros((hatch_delay, height, width), dtype=int)


def initialize_caterpillars(height, width):
    """
    Caterpillar counts per cell.
    """
    return np.zeros((height, width), dtype=int)


def random_positions(n_agents, height, width, rng):
    """
    Random integer grid positions for mobile agents.
    """
    xs = rng.integers(0, width, size=n_agents)
    ys = rng.integers(0, height, size=n_agents)
    return xs, ys