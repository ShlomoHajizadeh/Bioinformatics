"""
One-step orchestration for Version A.
"""

from core.clock import phase_of_day, is_night
from core.moth_dynamics import move_moths, deposit_eggs
from core.caterpillar_dynamics import (
    advance_egg_queue,
    add_hatched_caterpillars,
    apply_background_mortality,
)
from core.plant_dynamics import (
    apply_caterpillar_damage,
    recover_plants,
    clip_plant_health,
)
from core.predator_dynamics import move_predators, predator_feed


def step_version_a(state, params):
    """
    Perform one simulation step.

    Order:
    1. day/night determination
    2. moth movement
    3. egg laying at night
    4. egg hatching
    5. caterpillar mortality
    6. predator movement and feeding
    7. plant damage and recovery
    """
    step = state["step"]
    plant_health = state["plant_health"]
    eggs_queue = state["eggs_queue"]
    caterpillars = state["caterpillars"]
    moth_x = state["moth_x"]
    moth_y = state["moth_y"]
    pred_x = state["pred_x"]
    pred_y = state["pred_y"]
    rng = state["rng"]

    phase = phase_of_day(step, params.DAY_LENGTH, params.NIGHT_LENGTH)

    # Move moths every step, but egg laying only at night
    moth_x, moth_y = move_moths(
        moth_x,
        moth_y,
        plant_health,
        rng,
        move_radius=params.MOTH_MOVE_RADIUS,
        health_weight=params.MOTH_PREFERRED_HEALTH_WEIGHT,
    )

    if is_night(step, params.DAY_LENGTH, params.NIGHT_LENGTH):
        newly_laid_eggs = deposit_eggs(
            moth_x, moth_y, plant_health, rng, params.MOTH_EGG_LAYING_PROB
        )
    else:
        newly_laid_eggs = 0 * caterpillars

    eggs_queue, hatching = advance_egg_queue(eggs_queue, newly_laid_eggs)
    caterpillars = add_hatched_caterpillars(caterpillars, hatching)
    caterpillars = apply_background_mortality(
        caterpillars, params.CATERPILLAR_BACKGROUND_MORTALITY, rng
    )

    pred_x, pred_y = move_predators(
        pred_x,
        pred_y,
        caterpillars,
        rng,
        move_radius=params.PREDATOR_MOVE_RADIUS,
        prey_bias=params.PREDATOR_BIAS_TO_PREY,
    )

    caterpillars, predation = predator_feed(
        pred_x, pred_y, caterpillars, params.PREDATOR_CONSUMPTION_RATE
    )

    plant_health = apply_caterpillar_damage(
        plant_health, caterpillars, params.CATERPILLAR_DAMAGE_RATE
    )
    plant_health = recover_plants(
        plant_health, params.PLANT_RECOVERY_RATE, params.PLANT_MAX_HEALTH
    )
    plant_health = clip_plant_health(
        plant_health, params.PLANT_MIN_HEALTH, params.PLANT_MAX_HEALTH
    )

    state["step"] += 1
    state["phase"] = phase
    state["plant_health"] = plant_health
    state["eggs_queue"] = eggs_queue
    state["caterpillars"] = caterpillars
    state["moth_x"] = moth_x
    state["moth_y"] = moth_y
    state["pred_x"] = pred_x
    state["pred_y"] = pred_y
    state["predation"] = predation
    state["newly_laid_eggs"] = newly_laid_eggs
    state["hatching"] = hatching

    return state