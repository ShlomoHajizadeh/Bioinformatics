"""
Adult moth movement and egg laying.

In Version A:
- moths are mainly active at night
- they move locally
- they prefer healthier plants
- they lay eggs on the visited cell with some probability
"""

import numpy as np


def get_local_candidates(x, y, width, height, radius=1):
    """
    Return candidate cells in Moore neighborhood including current cell.
    """
    candidates = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            nx = (x + dx) % width
            ny = (y + dy) % height
            candidates.append((nx, ny))
    return candidates


def move_moths(moth_x, moth_y, plant_health, rng, move_radius=1, health_weight=1.0):
    """
    Move each moth to a nearby cell, biased toward healthier plants.
    """
    height, width = plant_health.shape
    new_x = moth_x.copy()
    new_y = moth_y.copy()

    for k in range(len(moth_x)):
        candidates = get_local_candidates(moth_x[k], moth_y[k], width, height, radius=move_radius)
        weights = []

        for cx, cy in candidates:
            w = 1e-6 + health_weight * plant_health[cy, cx]
            weights.append(w)

        weights = np.array(weights, dtype=float)
        weights /= weights.sum()

        idx = rng.choice(len(candidates), p=weights)
        chosen_x, chosen_y = candidates[idx]
        new_x[k] = chosen_x
        new_y[k] = chosen_y

    return new_x, new_y


def deposit_eggs(moth_x, moth_y, plant_health, rng, egg_prob):
    """
    Moths deposit eggs on their current cells with probability depending mildly on plant health.
    Returns an egg deposition array.
    """
    height, width = plant_health.shape
    eggs_new = np.zeros((height, width), dtype=int)

    for x, y in zip(moth_x, moth_y):
        p = egg_prob * (0.3 + 0.7 * plant_health[y, x])
        if rng.random() < p:
            eggs_new[y, x] += 1

    return eggs_new