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
        target, _ = find_nearest_target_for_male(
            agent,
            population.alive_agents(),
            environment,
            config.SENSING_RADIUS,
        )
        if target is not None:
            direction_to_target = environment.displacement(agent.position, target.position)
            direction_to_target = safe_normalize(direction_to_target)
            velocity = random_term + config.MALE_TARGETING_STRENGTH * direction_to_target

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