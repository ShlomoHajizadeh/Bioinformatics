import numpy as np

from core.enums import SexType
from core.utils import random_unit_vector_3d, safe_normalize, clip_norm


def find_nearest_target_for_male(agent, alive_agents, environment, sensing_radius):
    nearest_target = None
    nearest_distance = float("inf")

    for other in alive_agents:
        if other.agent_id == agent.agent_id or not other.alive:
            continue
        if other.sex_type not in {SexType.FEMALE, SexType.HERMAPHRODITE}:
            continue

        dist = environment.distance(agent.position, other.position)
        if dist <= sensing_radius and dist < nearest_distance:
            nearest_distance = dist
            nearest_target = other

    return nearest_target, nearest_distance


def update_agent_velocity(agent, population, environment, config, rng):
    random_direction = random_unit_vector_3d(rng)
    random_term = (
        config.RANDOM_MOTION_STRENGTH
        * (1.0 + config.STRESS_RANDOM_BOOST * agent.stress_level)
        * random_direction
    )

    velocity = random_term

    if agent.sex_type == SexType.MALE:
        target_term = np.zeros(3, dtype=float)
        pheromone_term = np.zeros(3, dtype=float)

        target, _ = find_nearest_target_for_male(
            agent,
            population.alive_agents(),
            environment,
            config.SENSING_RADIUS,
        )
        if target is not None:
            direction_to_target = environment.displacement(agent.position, target.position)
            target_term = config.MALE_TARGETING_STRENGTH * safe_normalize(direction_to_target)

        pheromone_gradient = environment.pheromone_gradient(agent.position)
        if np.linalg.norm(pheromone_gradient) > 0.0:
            pheromone_term = config.MALE_PHEROMONE_STRENGTH * safe_normalize(pheromone_gradient)

        velocity = random_term + target_term + pheromone_term

    velocity = safe_normalize(velocity) * config.BASE_SPEED
    velocity = clip_norm(velocity, config.MAX_SPEED)
    agent.velocity = velocity


def update_all_velocities(population, environment, config, rng):
    for agent in population.alive_agents():
        update_agent_velocity(agent, population, environment, config, rng)


def move_agent(agent, dt, environment):
    agent.position = agent.position + dt * agent.velocity
    agent.position, agent.velocity = environment.apply_boundaries(agent.position, agent.velocity)


def move_all_agents(population, dt, environment):
    for agent in population.alive_agents():
        move_agent(agent, dt, environment)