"""
Grid initialization utilities for Version B.
"""

import numpy as np


def initialize_plant_health(height, width, initial_health):
    return np.full((height, width), initial_health, dtype=float)


def initialize_attacked(height, width):
    return np.zeros((height, width), dtype=bool)


def initialize_defense_level(height, width):
    return np.zeros((height, width), dtype=float)


def initialize_bloom_mode(height, width, bloom_night_value):
    return np.full((height, width), bloom_night_value, dtype=int)


def initialize_egg_queues(height, width, hatch_delay):
    return np.zeros((hatch_delay, height, width), dtype=int)


def initialize_caterpillars(height, width):
    return np.zeros((height, width), dtype=int)


def random_positions(n_agents, height, width, rng):
    xs = rng.integers(0, width, size=n_agents)
    ys = rng.integers(0, height, size=n_agents)
    return xs, ys