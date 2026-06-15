"""
Airborne signaling, predator attractant, and priming for Version D.
"""

import numpy as np


def moore_neighborhood_average(field):
    total = np.zeros_like(field, dtype=float)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            total += np.roll(np.roll(field, dy, axis=0), dx, axis=1)
    return total / 9.0


def update_field(field, production_mask, production_rate, diffusion_rate, decay_rate, field_max):
    """
    Generic local field update with:
    - production on production_mask
    - Moore-neighborhood diffusion
    - decay
    """
    neighborhood_mean = moore_neighborhood_average(field)
    new_field = (
        (1.0 - decay_rate) * field
        + production_rate * production_mask.astype(float)
        + diffusion_rate * (neighborhood_mean - field)
    )
    return np.clip(new_field, 0.0, field_max)


def update_signal(signal, attacked, production_rate, diffusion_rate, decay_rate, signal_max):
    return update_field(
        signal,
        attacked,
        production_rate,
        diffusion_rate,
        decay_rate,
        signal_max,
    )


def update_predator_attractant(
    attractant,
    strong_defense_mask,
    production_rate,
    diffusion_rate,
    decay_rate,
    attractant_max,
):
    return update_field(
        attractant,
        strong_defense_mask,
        production_rate,
        diffusion_rate,
        decay_rate,
        attractant_max,
    )


def compute_priming_from_signal(signal, priming_strength, priming_max):
    priming = priming_strength * signal
    return np.clip(priming, 0.0, priming_max)