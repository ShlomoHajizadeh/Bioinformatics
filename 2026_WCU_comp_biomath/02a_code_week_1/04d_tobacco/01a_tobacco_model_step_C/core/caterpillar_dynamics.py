"""
Egg hatching, caterpillar updates, and mortality.
"""

import numpy as np


def advance_egg_queue(eggs_queue, newly_laid_eggs):
    """
    Shift the egg queue forward by one step.
    Eggs in layer 0 hatch now.
    Newly laid eggs enter the last layer.
    """
    hatching = eggs_queue[0].copy()
    eggs_queue[:-1] = eggs_queue[1:]
    eggs_queue[-1] = newly_laid_eggs
    return eggs_queue, hatching


def add_hatched_caterpillars(caterpillars, hatching_eggs):
    """
    Add newly hatched caterpillars to the grid.
    """
    return caterpillars + hatching_eggs


def apply_background_mortality(caterpillars, mortality_rate, rng):
    """
    Apply background mortality independently in each cell.
    """
    survivors = np.zeros_like(caterpillars)
    it = np.nditer(caterpillars, flags=["multi_index"])

    while not it.finished:
        n = int(it[0])
        survivors[it.multi_index] = rng.binomial(
            n, max(0.0, 1.0 - mortality_rate)
        )
        it.iternext()

    return survivors


def apply_defense_mortality(caterpillars, defense_level, max_extra_mortality, rng):
    """
    Apply additional caterpillar mortality on defended plants.

    If defense_level = 0, no extra mortality is applied.
    If defense_level = 1, the extra mortality is max_extra_mortality.

    Parameters
    ----------
    caterpillars : 2D int array
        Caterpillar counts per cell.
    defense_level : 2D float array
        Defense level in [0,1] per cell.
    max_extra_mortality : float
        Maximum extra mortality when defense_level = 1.
    rng : numpy random generator

    Returns
    -------
    survivors : 2D int array
        Updated caterpillar counts.
    """
    survivors = np.zeros_like(caterpillars)
    it = np.nditer(caterpillars, flags=["multi_index"])

    while not it.finished:
        idx = it.multi_index
        n = int(it[0])

        extra_mortality = max_extra_mortality * defense_level[idx]
        extra_mortality = min(max(extra_mortality, 0.0), 1.0)

        survive_prob = 1.0 - extra_mortality
        survivors[idx] = rng.binomial(n, survive_prob)

        it.iternext()

    return survivors