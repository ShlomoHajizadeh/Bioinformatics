"""
One-step orchestration for Version B.
"""

from core.clock import phase_of_day
from core.moth_dynamics import move_moths, deposit_eggs
from core.caterpillar_dynamics import (
    advance_egg_queue,
    add_hatched_caterpillars,
    apply_background_mortality,
)
from core.plant_dynamics import (
    update_attacked_status,
    update_defense_and_bloom,
    apply_caterpillar_damage,
    recover_plants,
    clip_plant_health,
)
from core.predator_dynamics import move_predators, predator_feed


def step_version_b(state, params):
    step = state["step"]
    rng = state["rng"]

    plant_health = state["plant_health"]
    attacked = state["attacked"]
    defense_level = state["defense_level"]
    bloom_mode = state["bloom_mode"]
    eggs_queue = state["eggs_queue"]
    caterpillars = state["caterpillars"]
    moth_x = state["moth_x"]
    moth_y = state["moth_y"]
    pred_x = state["pred_x"]
    pred_y = state["pred_y"]

    phase = phase_of_day(step, params.DAY_LENGTH, params.NIGHT_LENGTH)

    # 1. Moths move according to bloom mode and defense
    moth_x, moth_y = move_moths(
        moth_x,
        moth_y,
        plant_health,
        defense_level,
        bloom_mode,
        phase,
        rng,
        move_radius=params.MOTH_MOVE_RADIUS,
        health_weight=params.MOTH_PREFERRED_HEALTH_WEIGHT,
        bloom_weight=params.MOTH_PREFERRED_BLOOM_WEIGHT,
        defense_avoidance_weight=params.MOTH_DEFENSE_AVOIDANCE_WEIGHT,
        bloom_night_value=params.BLOOM_NIGHT,
        bloom_day_value=params.BLOOM_DAY,
    )

    # 2. Eggs are deposited every step, but favored by the correct bloom phase
    newly_laid_eggs = deposit_eggs(
        moth_x,
        moth_y,
        plant_health,
        defense_level,
        phase,
        bloom_mode,
        rng,
        params.MOTH_EGG_LAYING_PROB,
        bloom_night_value=params.BLOOM_NIGHT,
        bloom_day_value=params.BLOOM_DAY,
    )

    # 3. Eggs hatch and caterpillars update
    eggs_queue, hatching = advance_egg_queue(eggs_queue, newly_laid_eggs)
    caterpillars = add_hatched_caterpillars(caterpillars, hatching)
    caterpillars = apply_background_mortality(
        caterpillars, params.CATERPILLAR_BACKGROUND_MORTALITY, rng
    )

    # 4. Predators move and eat
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

    # 5. Plants detect attack and update defense
    attacked = update_attacked_status(caterpillars, params.ATTACK_THRESHOLD)
    defense_level, bloom_mode = update_defense_and_bloom(
        defense_level,
        bloom_mode,
        caterpillars,
        attacked,
        params.DEFENSE_ON_THRESHOLD,
        params.DEFENSE_OFF_THRESHOLD,
        params.DEFENSE_INCREASE_RATE,
        params.DEFENSE_RELAX_RATE,
        params.DEFENSE_MAX,
        params.BLOOM_NIGHT,
        params.BLOOM_DAY,
    )

    # 6. Plant damage and recovery
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
    state["attacked"] = attacked
    state["defense_level"] = defense_level
    state["bloom_mode"] = bloom_mode
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