import random
from collections import defaultdict

from environment.habitat import LAKE, RIVER, GRASSLAND


def build_cell_index(agents):
    cell_to_agents = defaultdict(list)

    for agent in agents:
        if agent.alive:
            cell_to_agents[(agent.x, agent.y)].append(agent)

    return cell_to_agents


def try_predation(predator, possible_prey, hunt_probability):
    if not predator.alive:
        return False, None

    alive_prey = [prey for prey in possible_prey if prey.alive]

    if len(alive_prey) == 0:
        return False, None

    if random.random() < hunt_probability:
        victim = random.choice(alive_prey)
        victim.alive = False
        return True, victim

    return False, None


def resolve_lake_interactions(agents_in_cell, params, kill_stats):
    native_trout = [a for a in agents_in_cell if a.alive and a.species == "NT"]
    invasive_trout = [a for a in agents_in_cell if a.alive and a.species == "IT"]
    birds = [a for a in agents_in_cell if a.alive and a.species == "P"]

    for predator in invasive_trout:
        success, _ = try_predation(predator, native_trout, params["IT_on_NT"])
        if success:
            kill_stats["IT_on_NT"] += 1

    for predator in birds:
        success, _ = try_predation(predator, native_trout, params["P_on_NT"])
        if success:
            predator.steps_since_nt_meal = 0
            kill_stats["P_on_NT"] += 1


def resolve_river_interactions(agents_in_cell, params, kill_stats):
    native_trout = [a for a in agents_in_cell if a.alive and a.species == "NT"]
    bears = [a for a in agents_in_cell if a.alive and a.species == "B"]

    for predator in bears:
        success, _ = try_predation(predator, native_trout, params["B_on_NT"])
        if success:
            predator.steps_since_bear_nt_meal = 0
            kill_stats["B_on_NT"] += 1


def resolve_grassland_interactions(agents_in_cell, params, kill_stats):
    elk = [a for a in agents_in_cell if a.alive and a.species == "E"]
    bears = [a for a in agents_in_cell if a.alive and a.species == "B"]

    for predator in bears:
        success, _ = try_predation(predator, elk, params["B_on_E"])
        if success:
            predator.steps_since_bear_e_meal = 0
            kill_stats["B_on_E"] += 1


def resolve_interactions(agents, lattice, params):
    cell_to_agents = build_cell_index(agents)

    kill_stats = {
        "IT_on_NT": 0,
        "P_on_NT": 0,
        "B_on_NT": 0,
        "B_on_E": 0
    }

    for (x, y), agents_in_cell in cell_to_agents.items():
        habitat = lattice.get_habitat(x, y)

        if habitat == LAKE:
            resolve_lake_interactions(agents_in_cell, params, kill_stats)
        elif habitat == RIVER:
            resolve_river_interactions(agents_in_cell, params, kill_stats)
        elif habitat == GRASSLAND:
            resolve_grassland_interactions(agents_in_cell, params, kill_stats)

    return kill_stats