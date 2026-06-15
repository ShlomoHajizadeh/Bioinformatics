import numpy as np

from core.agent import NematodeAgent
from core.enums import SexType, LifeStage
from core.utils import random_unit_vector_3d


def sample_offspring_sex(config, rng):
    r = rng.random()
    p_m = config.OFFSPRING_PROB_MALE
    p_f = config.OFFSPRING_PROB_FEMALE
    p_h = config.OFFSPRING_PROB_HERMAPHRODITE

    if abs((p_m + p_f + p_h) - 1.0) > 1e-10:
        raise ValueError("Offspring probabilities must sum to 1.")

    if r < p_m:
        return SexType.MALE
    elif r < p_m + p_f:
        return SexType.FEMALE
    return SexType.HERMAPHRODITE


def create_offspring(mother, next_id, config, rng):
    displacement = 0.5 * random_unit_vector_3d(rng)
    newborn_position = mother.position + displacement
    newborn_velocity = np.zeros(3, dtype=float)

    offspring = NematodeAgent(
        agent_id=next_id,
        sex_type=sample_offspring_sex(config, rng),
        life_stage=LifeStage.JUVENILE,
        position=newborn_position.astype(float),
        velocity=newborn_velocity,
        age=0.0,
        alive=True,
        stress_level=0.0,
        fertilized_by_male=False,
        time_since_last_birth=0.0,
    )
    return offspring


def reproduce_from_female(mother, environment, next_id, config, rng):
    newborns = []

    if not mother.can_give_birth():
        return newborns, next_id

    if not mother.fertilized_by_male:
        return newborns, next_id

    if not mother.ready_to_reproduce(config.REPRODUCTION_COOLDOWN):
        return newborns, next_id

    if mother.stress_level > 0.7:
        return newborns, next_id

    local_nutrient = environment.get_local_nutrient(mother.position)
    if local_nutrient < config.NUTRIENT_REPRODUCTION_CUTOFF:
        return newborns, next_id

    n_offspring = rng.integers(
        config.FEMALE_OFFSPRING_MIN,
        config.FEMALE_OFFSPRING_MAX + 1,
    )

    for _ in range(n_offspring):
        newborns.append(create_offspring(mother, next_id, config, rng))
        next_id += 1

    mother.reset_birth_clock()
    mother.fertilized_by_male = False
    return newborns, next_id


def reproduce_from_hermaphrodite(mother, environment, next_id, config, rng):
    newborns = []

    if not mother.can_give_birth():
        return newborns, next_id

    if not mother.ready_to_reproduce(config.REPRODUCTION_COOLDOWN):
        return newborns, next_id

    local_nutrient = environment.get_local_nutrient(mother.position)
    if local_nutrient < config.NUTRIENT_REPRODUCTION_CUTOFF:
        return newborns, next_id

    effective_selfing_prob = max(
        0.01,
        config.HERMAPHRODITE_SELFING_PROB * (1.0 - 0.5 * mother.stress_level),
    )

    if rng.random() >= effective_selfing_prob:
        return newborns, next_id

    n_offspring = rng.integers(
        config.HERMAPHRODITE_OFFSPRING_MIN,
        config.HERMAPHRODITE_OFFSPRING_MAX + 1,
    )

    for _ in range(n_offspring):
        newborns.append(create_offspring(mother, next_id, config, rng))
        next_id += 1

    mother.reset_birth_clock()
    return newborns, next_id


def process_reproduction(population, environment, config, next_id, rng):
    newborns = []

    for agent in population.alive_agents():
        if agent.sex_type == SexType.FEMALE:
            babies, next_id = reproduce_from_female(agent, environment, next_id, config, rng)
            newborns.extend(babies)

        elif agent.sex_type == SexType.HERMAPHRODITE:
            babies, next_id = reproduce_from_hermaphrodite(agent, environment, next_id, config, rng)
            newborns.extend(babies)

    for baby in newborns:
        baby.position, baby.velocity = environment.apply_boundaries(
            baby.position, baby.velocity
        )

    population.add_agents(newborns)
    return len(newborns), next_id