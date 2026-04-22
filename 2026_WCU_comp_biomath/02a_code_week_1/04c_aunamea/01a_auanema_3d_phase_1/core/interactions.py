from core.enums import SexType


def find_neighbors(agent, alive_agents, environment, radius):
    neighbors = []
    for other in alive_agents:
        if other.agent_id == agent.agent_id or not other.alive:
            continue
        if environment.distance(agent.position, other.position) <= radius:
            neighbors.append(other)
    return neighbors


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

            # male + female
            if agent.sex_type == SexType.MALE and other.sex_type == SexType.FEMALE:
                if rng.random() < config.FEMALE_FERTILIZATION_PROB:
                    other.fertilized_by_male = True

            elif agent.sex_type == SexType.FEMALE and other.sex_type == SexType.MALE:
                if rng.random() < config.FEMALE_FERTILIZATION_PROB:
                    agent.fertilized_by_male = True

            # male + hermaphrodite encounter
            # currently only noted indirectly by proximity; no extra state needed
            # but could easily be extended later