"""
Adult moth movement and egg laying for Version B.

New in Version B:
- moths prefer plants whose bloom matches the current time:
    night-blooming plants at night
    day-blooming plants during day
- moths avoid defended plants
- egg laying is reduced on defended plants
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


def bloom_match_score(bloom_value, phase, bloom_night_value, bloom_day_value):
    if phase == "night" and bloom_value == bloom_night_value:
        return 1.0
    if phase == "day" and bloom_value == bloom_day_value:
        return 1.0
    return 0.0


def move_moths(
    moth_x,
    moth_y,
    plant_health,
    defense_level,
    bloom_mode,
    phase,
    rng,
    move_radius=1,
    health_weight=1.0,
    bloom_weight=2.0,
    defense_avoidance_weight=2.5,
    bloom_night_value=0,
    bloom_day_value=1,
):
    """
    Move moths to nearby cells.

    Preference:
    - healthier plants
    - plants blooming in the current phase
    - lower defense levels
    """
    height, width = plant_health.shape
    new_x = moth_x.copy()
    new_y = moth_y.copy()

    for k in range(len(moth_x)):
        candidates = get_local_candidates(
            moth_x[k], moth_y[k], width, height, radius=move_radius
        )

        weights = []
        for cx, cy in candidates:
            bloom_bonus = bloom_match_score(
                bloom_mode[cy, cx],
                phase,
                bloom_night_value,
                bloom_day_value,
            )

            w = (
                1e-6
                + health_weight * plant_health[cy, cx]
                + bloom_weight * bloom_bonus
                + defense_avoidance_weight * (1.0 - defense_level[cy, cx])
            )
            weights.append(max(w, 1e-6))

        weights = np.array(weights, dtype=float)
        weights /= weights.sum()

        idx = rng.choice(len(candidates), p=weights)
        chosen_x, chosen_y = candidates[idx]
        new_x[k] = chosen_x
        new_y[k] = chosen_y

    return new_x, new_y


def deposit_eggs(
    moth_x,
    moth_y,
    plant_health,
    defense_level,
    phase,
    bloom_mode,
    rng,
    egg_prob,
    bloom_night_value=0,
    bloom_day_value=1,
):
    """
    Moths deposit eggs with reduced probability on defended plants.

    A bloom-phase mismatch also reduces egg laying.
    """
    height, width = plant_health.shape
    eggs_new = np.zeros((height, width), dtype=int)

    for x, y in zip(moth_x, moth_y):
        phase_match = bloom_match_score(
            bloom_mode[y, x], phase, bloom_night_value, bloom_day_value
        )

        p = (
            egg_prob
            * (0.3 + 0.7 * plant_health[y, x])
            * (1.0 - 0.8 * defense_level[y, x])
            * (0.3 + 0.7 * phase_match)
        )

        p = min(max(p, 0.0), 1.0)

        if rng.random() < p:
            eggs_new[y, x] += 1

    return eggs_new