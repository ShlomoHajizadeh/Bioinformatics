"""
Predator movement and predation for Version D.
"""

import numpy as np


def get_local_candidates(x, y, width, height, radius=1):
    candidates = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            nx = (x + dx) % width
            ny = (y + dy) % height
            candidates.append((nx, ny))
    return candidates


def move_predators(
    pred_x,
    pred_y,
    caterpillars,
    predator_attractant,
    rng,
    move_radius=1,
    prey_bias=2.0,
    attractant_bias=4.0,
):
    """
    Predators move toward prey-rich and chemically attractive cells.
    """
    height, width = caterpillars.shape
    new_x = pred_x.copy()
    new_y = pred_y.copy()

    for k in range(len(pred_x)):
        candidates = get_local_candidates(
            pred_x[k], pred_y[k], width, height, radius=move_radius
        )

        weights = []
        for cx, cy in candidates:
            w = (
                1.0
                + prey_bias * caterpillars[cy, cx]
                + attractant_bias * predator_attractant[cy, cx]
            )
            weights.append(w)

        weights = np.array(weights, dtype=float)
        weights /= weights.sum()

        idx = rng.choice(len(candidates), p=weights)
        chosen_x, chosen_y = candidates[idx]
        new_x[k] = chosen_x
        new_y[k] = chosen_y

    return new_x, new_y


def predator_feed(pred_x, pred_y, caterpillars, consumption_rate):
    predation = np.zeros_like(caterpillars)

    for x, y in zip(pred_x, pred_y):
        available = caterpillars[y, x]
        eaten = min(available, consumption_rate)
        caterpillars[y, x] -= eaten
        predation[y, x] += eaten

    return caterpillars, predation