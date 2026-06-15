"""
Airborne signaling and priming for Version C.

We model:
- volatile_signal: produced by attacked plants
- simple neighborhood spreading using Moore-neighborhood averaging
- decay over time
- priming derived from signal strength
"""

import numpy as np


def moore_neighborhood_average(field):
    """
    Compute Moore-neighborhood average with periodic boundary conditions.
    """
    total = np.zeros_like(field, dtype=float)

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            total += np.roll(np.roll(field, dy, axis=0), dx, axis=1)

    return total / 9.0


def update_signal(
    signal,
    attacked,
    production_rate,
    diffusion_rate,
    decay_rate,
    signal_max,
):
    """
    Update airborne signal field.

    Components:
    - existing signal decays
    - attacked plants produce signal
    - signal spreads locally through neighborhood averaging
    """
    neighborhood_mean = moore_neighborhood_average(signal)

    new_signal = (
        (1.0 - decay_rate) * signal
        + production_rate * attacked.astype(float)
        + diffusion_rate * (neighborhood_mean - signal)
    )

    new_signal = np.clip(new_signal, 0.0, signal_max)
    return new_signal


def compute_priming_from_signal(signal, priming_strength, priming_max):
    """
    Convert signal to priming level in [0, priming_max].
    """
    priming = priming_strength * signal
    priming = np.clip(priming, 0.0, priming_max)
    return priming