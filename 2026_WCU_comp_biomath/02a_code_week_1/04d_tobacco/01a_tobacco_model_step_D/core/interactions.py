"""
One-step orchestration for Version D.
"""

from core.clock import phase_of_day
from core.moth_dynamics import move_moths, deposit_eggs
from core.caterpillar_dynamics import (
    advance_egg_queue,
    add_hatched_caterpillars,
    apply_background_mortality,
    apply_defense_mortality,
    apply_growth_inhibitor_mortality,
)
from core.plant_dynamics import (
    update_attacked_status,
    update_defense_and_bloom,
    update_growth_inhibitor,
    apply_caterpillar_damage,
    recover_plants,
    clip_plant_health,
)
from core.predator_dynamics import move_predators, predator_feed
from core.signaling import (
    update_signal,
    update_predator_attractant,
    compute_priming_from_signal,
)


def step_version_d(state, params):
    step = state["step"]
    rng = state["rng"]

    plant_health = state["plant_health"]
    attacked = state["attacked"]
    defense_level = state["defense_level"]
    bloom_mode = state["bloom_mode"]
    signal = state["signal"]
    priming = state["priming"]
    predator_attractant = state["predator_attractant"]
    growth_inhibitor = state["growth_inhibitor"]
    eggs_queue = state["eggs_queue"]
    caterpillars = state["caterpillars"]
    moth_x = state["moth_x"]
    moth_y = state["moth_y"]
    pred_x = state["pred_x"]
    pred_y = state["pred_y"]

    phase = phase_of_day(step, params.DAY_LENGTH, params.NIGHT_LENGTH)

    # 1. Moths move
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

    # 2. Eggs are deposited
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

    # 4. Baseline and plant-mediated caterpillar mortality
    caterpillars = apply_background_mortality(
        caterpillars,
        params.CATERPILLAR_BACKGROUND_MORTALITY,
        rng,
    )
    caterpillars = apply_defense_mortality(
        caterpillars,
        defense_level,
        params.DEFENSE_CATERPILLAR_MORTALITY,
        rng,
    )
    caterpillars = apply_growth_inhibitor_mortality(
        caterpillars,
        growth_inhibitor,
        params.GROWTH_INHIBITOR_CATERPILLAR_MORTALITY,
        rng,
    )

    # 5. Determine attacked plants
    attacked = update_attacked_status(caterpillars, params.ATTACK_THRESHOLD)

    # 6. Warning signal and priming
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

    # 7. Defense and bloom switching
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

    # 8. Growth inhibitor and predator attractant production
    growth_inhibitor = update_growth_inhibitor(
        growth_inhibitor,
        defense_level,
        increase_rate=params.GROWTH_INHIBITOR_INCREASE_RATE,
        relax_rate=params.GROWTH_INHIBITOR_RELAX_RATE,
        inhibitor_max=params.GROWTH_INHIBITOR_MAX,
    )

    predator_attractant = update_predator_attractant(
        predator_attractant,
        defense_level >= 0.20,
        production_rate=params.ATTRACTANT_PRODUCTION_RATE,
        diffusion_rate=params.ATTRACTANT_DIFFUSION_RATE,
        decay_rate=params.ATTRACTANT_DECAY_RATE,
        attractant_max=params.ATTRACTANT_MAX,
    )

    # 9. Predators move and feed
    pred_x, pred_y = move_predators(
        pred_x,
        pred_y,
        caterpillars,
        predator_attractant,
        rng,
        move_radius=params.PREDATOR_MOVE_RADIUS,
        prey_bias=params.PREDATOR_BIAS_TO_PREY,
        attractant_bias=params.PREDATOR_BIAS_TO_ATTRACTANT,
    )
    caterpillars, predation = predator_feed(
        pred_x,
        pred_y,
        caterpillars,
        params.PREDATOR_CONSUMPTION_RATE,
    )

    # 10. Plant damage and recovery
    plant_health = apply_caterpillar_damage(
        plant_health,
        caterpillars,
        params.CATERPILLAR_DAMAGE_RATE,
        growth_inhibitor,
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

    state["step"] += 1
    state["phase"] = phase
    state["plant_health"] = plant_health
    state["attacked"] = attacked
    state["defense_level"] = defense_level
    state["bloom_mode"] = bloom_mode
    state["signal"] = signal
    state["priming"] = priming
    state["predator_attractant"] = predator_attractant
    state["growth_inhibitor"] = growth_inhibitor
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