"""
Plant damage and recovery.
"""

import numpy as np


def apply_caterpillar_damage(plant_health, caterpillars, damage_rate):
    """
    Damage plants according to local caterpillar counts.
    """
    damage = damage_rate * caterpillars
    plant_health = plant_health - damage
    return plant_health


def recover_plants(plant_health, recovery_rate, max_health):
    """
    Slow recovery toward max health.
    """
    damaged_mask = plant_health < max_health
    plant_health[damaged_mask] += recovery_rate
    plant_health = np.clip(plant_health, 0.0, max_health)
    return plant_health


def clip_plant_health(plant_health, min_health=0.0, max_health=1.0):
    return np.clip(plant_health, min_health, max_health)