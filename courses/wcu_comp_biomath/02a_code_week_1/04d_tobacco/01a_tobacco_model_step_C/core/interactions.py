"""
One-step orchestration for Version C.
"""

from core.clock import phase_of_day
from core.moth_dynamics import move_moths, deposit_eggs
from core.caterpillar_dynamics import (
    advance_egg_queue,
    add_hatched_caterpillars,
    apply_background_mortality,
    apply_defense_mortality,
)
from core.plant_dynamics import (
    update_attacked_status,
    update_defense_and_bloom,
    apply_caterpillar_damage,
    recover_plants,
    clip_plant_health,
)
from core.predator_dynamics import move_predators, predator_feed
from core.signaling import update_signal, compute_priming_from_signal


def step_version_c(state, params):
    """
    Perform one full simulation step for Version C.

    Order:
    1. Determine day/night phase
    2. Move moths
    3. Deposit eggs
    4. Hatch eggs and update caterpillars
    5. Apply background and defense-dependent caterpillar mortality
    6. Move predators and apply predation
    7. Update attacked plants
    8. Update volatile signal and priming
    9. Update plant defense and bloom mode
    10. Apply plant damage and recovery
    """
    step = state["step"]
    rng = state["rng"]

    plant_health = state["plant_health"]
    attacked = state["attacked"]
    defense_level = state["defense_level"]
    bloom_mode = state["bloom_mode"]
    signal = state["signal"]
    priming = state["priming"]
    eggs_queue = state["eggs_queue"]
    caterpillars = state["caterpillars"]
    moth_x = state["moth_x"]
    moth_y = state["moth_y"]
    pred_x = state["pred_x"]
    pred_y = state["pred_y"]

    phase = phase_of_day(step, params.DAY_LENGTH, params.NIGHT_LENGTH)

    # 1. Moths move according to plant health, bloom mode, and defense
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

    # 2. Moths deposit eggs
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

    # 3. Egg hatching and caterpillar update
    eggs_queue, hatching = advance_egg_queue(eggs_queue, newly_laid_eggs)
    caterpillars = add_hatched_caterpillars(caterpillars, hatching)

    # 4. Background mortality
    caterpillars = apply_background_mortality(
        caterpillars,
        params.CATERPILLAR_BACKGROUND_MORTALITY,
        rng,
    )

    # 5. Extra mortality on defended plants
    caterpillars = apply_defense_mortality(
        caterpillars,
        defense_level,
        params.DEFENSE_CATERPILLAR_MORTALITY,
        rng,
    )

    # 6. Predator movement and predation
    pred_x, pred_y = move_predators(
        pred_x,
        pred_y,
        caterpillars,
        rng,
        move_radius=params.PREDATOR_MOVE_RADIUS,
        prey_bias=params.PREDATOR_BIAS_TO_PREY,
    )
    caterpillars, predation = predator_feed(
        pred_x,
        pred_y,
        caterpillars,
        params.PREDATOR_CONSUMPTION_RATE,
    )

    # 7. Update attacked plants
    attacked = update_attacked_status(caterpillars, params.ATTACK_THRESHOLD)

    # 8. Update signaling and priming
    signal = update_signal(
        signal,
        attacked,
        production_rate=params.SIGNAL_PRODUCTION_RATE,
        diffusion_rate=params.SIGNAL_DIFFUSION_RATE,
        decay_rate=params.SIGNAL_DECAY_RATE,
        signal_max=params.SIGNAL_MAX,
    )
    priming = compute_priming_from_signal(
        signal,
        priming_strength=params.PRIMING_STRENGTH,
        priming_max=params.PRIMING_MAX,
    )

    # 9. Update defense and bloom mode using priming
    defense_level, bloom_mode, effective_threshold = update_defense_and_bloom(
        defense_level,
        bloom_mode,
        caterpillars,
        priming,
        params.DEFENSE_ON_THRESHOLD,
        params.DEFENSE_OFF_THRESHOLD,
        params.DEFENSE_INCREASE_RATE,
        params.DEFENSE_RELAX_RATE,
        params.DEFENSE_MAX,
        params.BLOOM_NIGHT,
        params.BLOOM_DAY,
    )

    # 10. Apply plant damage and recovery
    plant_health = apply_caterpillar_damage(
        plant_health,
        caterpillars,
        params.CATERPILLAR_DAMAGE_RATE,
    )
    plant_health = recover_plants(
        plant_health,
        params.PLANT_RECOVERY_RATE,
        params.PLANT_MAX_HEALTH,
    )
    plant_health = clip_plant_health(
        plant_health,
        params.PLANT_MIN_HEALTH,
        params.PLANT_MAX_HEALTH,
    )

    # Write back updated state
    state["step"] += 1
    state["phase"] = phase
    state["plant_health"] = plant_health
    state["attacked"] = attacked
    state["defense_level"] = defense_level
    state["bloom_mode"] = bloom_mode
    state["signal"] = signal
    state["priming"] = priming
    state["effective_threshold"] = effective_threshold
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