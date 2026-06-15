from core.enums import SexType, LifeStage


def find_neighbors(agent, alive_agents, environment, radius):
    neighbors = []
    for other in alive_agents:
        if other.agent_id == agent.agent_id or not other.alive:
            continue
        if environment.distance(agent.position, other.position) <= radius:
            neighbors.append(other)
    return neighbors


def nutrient_consumption_for_stage(agent, config):
    if agent.life_stage == LifeStage.JUVENILE:
        return config.NUTRIENT_CONSUMPTION_JUVENILE
    if agent.life_stage == LifeStage.ADULT:
        return config.NUTRIENT_CONSUMPTION_ADULT
    return config.NUTRIENT_CONSUMPTION_REPRODUCTIVE


def update_environment_agent_coupling(population, environment, config):
    for agent in population.alive_agents():
        required = nutrient_consumption_for_stage(agent, config)
        consumed = environment.consume_nutrient(agent.position, required)

        if consumed < required:
            deficit_ratio = 1.0 - consumed / max(required, 1e-12)
            agent.stress_level += config.LOW_NUTRIENT_STRESS_INCREASE * deficit_ratio

        local_nutrient = environment.get_local_nutrient(agent.position)
        if local_nutrient < config.LOW_NUTRIENT_THRESHOLD:
            agent.stress_level += config.LOW_NUTRIENT_STRESS_INCREASE

        if agent.sex_type == SexType.FEMALE:
            environment.deposit_pheromone(agent.position, config.FEMALE_PHEROMONE_DEPOSIT)
        elif agent.sex_type == SexType.HERMAPHRODITE:
            environment.deposit_pheromone(agent.position, config.HERMAPHRODITE_PHEROMONE_DEPOSIT)

        agent.stress_level = max(0.0, min(config.MAX_STRESS, agent.stress_level))


def update_stress_from_crowding(population, environment, config):
    alive = population.alive_agents()
    for agent in alive:
        neighbors = find_neighbors(agent, alive, environment, config.CROWDING_RADIUS)
        crowding = len(neighbors)
        agent.stress_level += config.CROWDING_STRESS_FACTOR * crowding
        agent.stress_level -= config.STRESS_DECAY
        agent.stress_level = max(0.0, min(config.MAX_STRESS, agent.stress_level))


def process_pairwise_interactions(population, environment, config, rng):
    alive = population.alive_agents()

    for agent in alive:
        if not agent.can_mate():
            continue

        for other in alive:
            if other.agent_id <= agent.agent_id or not other.can_mate():
                continue

            distance = environment.distance(agent.position, other.position)
            if distance > config.MATING_RADIUS:
                continue

            if agent.sex_type == SexType.MALE and other.sex_type == SexType.FEMALE:
                if rng.random() < config.FEMALE_FERTILIZATION_PROB:
                    other.fertilized_by_male = True

            elif agent.sex_type == SexType.FEMALE and other.sex_type == SexType.MALE:
                if rng.random() < config.FEMALE_FERTILIZATION_PROB:
                    agent.fertilized_by_male = True