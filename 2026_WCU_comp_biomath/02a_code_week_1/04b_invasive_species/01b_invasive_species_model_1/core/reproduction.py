import numpy as np

from agents.base_agent import BaseAgent


def count_alive_by_species(agents, species):
    return sum(1 for agent in agents if agent.alive and agent.species == species)


def get_alive_parents(agents, species):
    return [agent for agent in agents if agent.alive and agent.species == species]


def place_offspring_near_parent(parent, lattice):
    """
    Place offspring at parent position if valid, otherwise use a valid neighbor.
    """
    allowed = parent.allowed_habitats()

    if lattice.get_habitat(parent.x, parent.y) in allowed:
        return parent.x, parent.y

    candidate_moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for dx, dy in candidate_moves:
        nx, ny = lattice.wrap(parent.x + dx, parent.y + dy)
        if lattice.get_habitat(nx, ny) in allowed:
            return nx, ny

    return parent.x, parent.y


def apply_reproduction(agents, lattice, birth_rates):
    """
    Stochastic births proportional to current population sizes.

    Returns
    -------
    (agents, birth_stats)
    """
    species_list = ["NT", "IT", "B", "P", "E"]
    birth_stats = {species: 0 for species in species_list}

    new_agents = []

    for species in species_list:
        population = count_alive_by_species(agents, species)
        if population <= 0:
            continue

        rate = birth_rates[species]
        num_births = np.random.binomial(population, rate)

        parents = get_alive_parents(agents, species)
        if len(parents) == 0:
            continue

        for _ in range(num_births):
            parent = parents[np.random.randint(len(parents))]
            x, y = place_offspring_near_parent(parent, lattice)
            offspring = BaseAgent(species, x, y)
            new_agents.append(offspring)
            birth_stats[species] += 1

    agents.extend(new_agents)
    return agents, birth_stats