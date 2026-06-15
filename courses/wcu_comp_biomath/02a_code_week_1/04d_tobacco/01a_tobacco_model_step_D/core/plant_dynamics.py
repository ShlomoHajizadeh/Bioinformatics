"""
Plant damage, recovery, inducible defense, priming, and growth inhibitor for Version D.
"""

import numpy as np


def update_attacked_status(caterpillars, attack_threshold):
    return caterpillars >= attack_threshold


def update_defense_and_bloom(
    defense_level,
    bloom_mode,
    caterpillars,
    priming,
    defense_on_threshold,
    defense_off_threshold,
    defense_increase_rate,
    defense_relax_rate,
    defense_max,
    bloom_night_value,
    bloom_day_value,
):
    """
    Priming lowers the effective defense activation threshold.
    """
    defense_level = defense_level.copy()

    effective_threshold = np.maximum(
        1.0,
        defense_on_threshold * (1.0 - 1.4 * priming)
    )

    high_pressure = caterpillars >= effective_threshold
    low_pressure = caterpillars <= defense_off_threshold

    defense_level[high_pressure] += defense_increase_rate
    defense_level[low_pressure] -= defense_relax_rate

    defense_level = np.clip(defense_level, 0.0, defense_max)
    bloom_mode = np.where(defense_level > 0.0, bloom_day_value, bloom_night_value)

    return defense_level, bloom_mode, effective_threshold


def update_growth_inhibitor(
    growth_inhibitor,
    defense_level,
    increase_rate,
    relax_rate,
    inhibitor_max,
):
    """
    Growth inhibitor is produced on sufficiently defended plants and relaxes otherwise.
    """
    growth_inhibitor = growth_inhibitor.copy()

    strong_defense = defense_level >= 0.20
    weak_defense = defense_level < 0.10

    growth_inhibitor[strong_defense] += increase_rate
    growth_inhibitor[weak_defense] -= relax_rate

    return np.clip(growth_inhibitor, 0.0, inhibitor_max)


def apply_caterpillar_damage(plant_health, caterpillars, damage_rate, growth_inhibitor):
    """
    Growth inhibitor reduces effective feeding damage.
    """
    effective_damage = damage_rate * caterpillars * (1.0 - 0.5 * growth_inhibitor)
    return plant_health - effective_damage


def recover_plants(plant_health, recovery_rate, max_health):
    damaged_mask = plant_health < max_health
    plant_health[damaged_mask] += recovery_rate
    return np.clip(plant_health, 0.0, max_health)


def clip_plant_health(plant_health, min_health=0.0, max_health=1.0):
    return np.clip(plant_health, min_health, max_health)