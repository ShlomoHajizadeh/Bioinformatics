import copy
import numpy as np

from core.agent import NematodeAgent
from core.enums import SexType, LifeStage
from core.population import Population
from core.environment import Environment3D
from core.movement import update_all_velocities, move_all_agents
from core.interactions import (
    process_pairwise_interactions,
    update_stress_from_crowding,
    update_environment_agent_coupling,
)
from core.reproduction import process_reproduction
from core.aging import age_all_agents
from core.mortality import apply_mortality
from output.statistics import SimulationStatistics


def initialize_population(config, rng):
    agents = []
    next_id = 0

    def random_position():
        return np.array([
            rng.uniform(0, config.DOMAIN_X),
            rng.uniform(0, config.DOMAIN_Y),
            rng.uniform(0, config.DOMAIN_Z),
        ], dtype=float)

    def zero_velocity():
        return np.zeros(3, dtype=float)

    for _ in range(config.INITIAL_MALES):
        agents.append(
            NematodeAgent(
                agent_id=next_id,
                sex_type=SexType.MALE,
                life_stage=LifeStage.ADULT,
                position=random_position(),
                velocity=zero_velocity(),
                age=config.JUVENILE_AGE_THRESHOLD + 0.5,
            )
        )
        next_id += 1

    for _ in range(config.INITIAL_FEMALES):
        agents.append(
            NematodeAgent(
                agent_id=next_id,
                sex_type=SexType.FEMALE,
                life_stage=LifeStage.ADULT,
                position=random_position(),
                velocity=zero_velocity(),
                age=config.JUVENILE_AGE_THRESHOLD + 0.5,
            )
        )
        next_id += 1

    for _ in range(config.INITIAL_HERMAPHRODITES):
        agents.append(
            NematodeAgent(
                agent_id=next_id,
                sex_type=SexType.HERMAPHRODITE,
                life_stage=LifeStage.ADULT,
                position=random_position(),
                velocity=zero_velocity(),
                age=config.JUVENILE_AGE_THRESHOLD + 0.5,
            )
        )
        next_id += 1

    return Population(agents), next_id


def run_simulation(config):
    rng = np.random.default_rng(config.RANDOM_SEED)

    environment = Environment3D(
        x_size=config.DOMAIN_X,
        y_size=config.DOMAIN_Y,
        z_size=config.DOMAIN_Z,
        periodic=config.PERIODIC_BOUNDARIES,
        grid_shape=(config.GRID_NX, config.GRID_NY, config.GRID_NZ),
        initial_nutrient_level=config.INITIAL_NUTRIENT_LEVEL,
    )

    population, next_id = initialize_population(config, rng)
    stats = SimulationStatistics()
    history_snapshots = []

    for step in range(config.N_STEPS):
        t = step * config.DT

        environment.regenerate_nutrients(
            regen_rate=config.NUTRIENT_REGEN_RATE,
            nutrient_max=config.NUTRIENT_MAX,
        )
        environment.diffuse_and_decay_pheromones(
            diffusion_strength=config.PHEROMONE_DIFFUSION_STRENGTH,
            decay_rate=config.PHEROMONE_DECAY_RATE,
            pheromone_max=config.PHEROMONE_MAX,
        )

        update_all_velocities(population, environment, config, rng)
        move_all_agents(population, config.DT, environment)

        update_environment_agent_coupling(population, environment, config)
        update_stress_from_crowding(population, environment, config)
        process_pairwise_interactions(population, environment, config, rng)

        births, next_id = process_reproduction(population, environment, config, next_id, rng)

        age_all_agents(population, config.DT, config)
        deaths = apply_mortality(population, config, rng)

        stats.record(t, population, environment, births, deaths)

        if config.SAVE_ANIMATION and step % config.ANIMATION_EVERY_N_STEPS == 0:
            history_snapshots.append(copy.deepcopy(population.alive_agents()))

        if config.VERBOSE and step % config.PRINT_EVERY == 0:
            print(
                f"Step {step:4d} | "
                f"t = {t:6.2f} | "
                f"total = {population.count_total():4d} | "
                f"m = {population.count_by_sex(SexType.MALE):4d} | "
                f"f = {population.count_by_sex(SexType.FEMALE):4d} | "
                f"h = {population.count_by_sex(SexType.HERMAPHRODITE):4d} | "
                f"births = {births:3d} | deaths = {deaths:3d} | "
                f"nut = {environment.mean_nutrient():.2f} | "
                f"pher = {environment.mean_pheromone():.2f}"
            )

    return population, environment, stats, history_snapshots