"""
Plant damage, recovery, and inducible defense for Version B.
"""

import numpy as np


def update_attacked_status(caterpillars, attack_threshold):
    """
    A plant is marked as attacked if local caterpillar count is large enough.
    """
    return caterpillars >= attack_threshold


def update_defense_and_bloom(
    defense_level,
    bloom_mode,
    caterpillars,
    attacked,
    defense_on_threshold,
    defense_off_threshold,
    defense_increase_rate,
    defense_relax_rate,
    defense_max,
    bloom_night_value,
    bloom_day_value,
):
    """
    Update defense level and bloom mode.

    Rules:
    - If caterpillars are above defense_on_threshold, defense increases.
    - If caterpillars are below defense_off_threshold, defense relaxes.
    - Otherwise keep current level.
    - Plants with positive defense_level bloom during day.
    - Plants with zero defense_level bloom during night.
    """
    defense_level = defense_level.copy()

    high_pressure = caterpillars >= defense_on_threshold
    low_pressure = caterpillars <= defense_off_threshold

    defense_level[high_pressure] += defense_increase_rate
    defense_level[low_pressure] -= defense_relax_rate

    defense_level = np.clip(defense_level, 0.0, defense_max)

    bloom_mode = np.where(defense_level > 0.0, bloom_day_value, bloom_night_value)

    return defense_level, bloom_mode


def apply_caterpillar_damage(plant_health, caterpillars, damage_rate):
    damage = damage_rate * caterpillars
    return plant_health - damage


def recover_plants(plant_health, recovery_rate, max_health):
    damaged_mask = plant_health < max_health
    plant_health[damaged_mask] += recovery_rate
    return np.clip(plant_health, 0.0, max_health)


def clip_plant_health(plant_health, min_health=0.0, max_health=1.0):
    return np.clip(plant_health, min_health, max_health)