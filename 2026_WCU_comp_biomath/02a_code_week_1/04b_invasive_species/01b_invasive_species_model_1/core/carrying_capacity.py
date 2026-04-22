import random


def enforce_species_capacity(agents, species, capacity):
    alive_species = [agent for agent in agents if agent.alive and agent.species == species]

    if len(alive_species) <= capacity:
        return 0

    excess = len(alive_species) - capacity
    to_remove = random.sample(alive_species, excess)

    for agent in to_remove:
        agent.alive = False

    return excess


def apply_carrying_capacity(agents, capacities):
    """
    Enforce total carrying capacities.

    Returns
    -------
    dict
        Number removed due to carrying capacity.
    """
    removed_stats = {}

    for species, cap in capacities.items():
        removed = enforce_species_capacity(agents, species, cap)
        removed_stats[f"cap_{species}"] = removed

    return removed_stats