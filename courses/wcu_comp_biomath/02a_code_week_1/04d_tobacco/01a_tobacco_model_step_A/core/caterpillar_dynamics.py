"""
Egg hatching, caterpillar updates, and mortality.
"""

import numpy as np


def advance_egg_queue(eggs_queue, newly_laid_eggs):
    """
    Shift egg queue forward by one step.
    Eggs in layer 0 hatch now.
    Newly laid eggs enter the last layer.
    """
    hatching = eggs_queue[0].copy()
    eggs_queue[:-1] = eggs_queue[1:]
    eggs_queue[-1] = newly_laid_eggs
    return eggs_queue, hatching


def add_hatched_caterpillars(caterpillars, hatching_eggs):
    """
    New caterpillars are added from hatching eggs.
    """
    return caterpillars + hatching_eggs


def apply_background_mortality(caterpillars, mortality_rate, rng):
    """
    Binomial survival step.
    """
    survivors = np.zeros_like(caterpillars)
    it = np.nditer(caterpillars, flags=["multi_index"])
    while not it.finished:
        n = int(it[0])
        survivors[it.multi_index] = rng.binomial(n, max(0.0, 1.0 - mortality_rate))
        it.iternext()
    return survivors