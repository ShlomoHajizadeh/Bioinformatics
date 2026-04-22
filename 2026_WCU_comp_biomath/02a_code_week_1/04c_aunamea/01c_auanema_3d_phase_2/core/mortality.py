from core.enums import SexType, LifeStage


def lifespan_for_agent(agent, config):
    if agent.sex_type == SexType.MALE:
        return config.MALE_LIFESPAN
    if agent.sex_type == SexType.FEMALE:
        return config.FEMALE_LIFESPAN
    return config.HERMAPHRODITE_LIFESPAN


def apply_mortality(population, config, rng):
    for agent in population.alive_agents():
        # age-based death
        if agent.age >= lifespan_for_agent(agent, config):
            agent.alive = False
            continue

        # juvenile mortality
        if agent.life_stage == LifeStage.JUVENILE:
            if rng.random() < config.JUVENILE_DEATH_PROB:
                agent.alive = False
                continue

        # stress-based mortality
        stress_death_prob = config.ADULT_STRESS_DEATH_PROB_FACTOR * agent.stress_level
        if rng.random() < stress_death_prob:
            agent.alive = False

    removed = population.remove_dead()
    return removed