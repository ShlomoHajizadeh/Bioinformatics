"""
Utility functions for the chase-and-escape simulation
"""

import random
import numpy as np


def set_random_seed(seed):
    """
    Set Python and NumPy random seeds.
    """
    random.seed(seed)
    np.random.seed(seed)


def count_alive_targets(targets):
    """
    Count how many targets are still alive.
    """
    return sum(target.alive for target in targets.values())


def count_occupied_sites(grid):
    """
    Count the number of occupied lattice sites.
    """
    return np.sum(grid != 0)


def validate_positions(agents, LX, LY):
    """
    Check that all agent positions lie inside the lattice.
    Raises AssertionError if not.
    """
    for agent in agents.values():
        assert 0 <= agent.x < LX, f"x-position out of bounds: {agent.x}"
        assert 0 <= agent.y < LY, f"y-position out of bounds: {agent.y}"


def validate_unique_positions(targets, chasers):
    """
    Check that no two agents occupy the same site.
    Raises AssertionError if overlap is found.
    """
    positions = set()

    for target in targets.values():
        if target.alive:
            pos = (target.x, target.y)
            assert pos not in positions, f"Duplicate position found: {pos}"
            positions.add(pos)

    for chaser in chasers.values():
        pos = (chaser.x, chaser.y)
        assert pos not in positions, f"Duplicate position found: {pos}"
        positions.add(pos)