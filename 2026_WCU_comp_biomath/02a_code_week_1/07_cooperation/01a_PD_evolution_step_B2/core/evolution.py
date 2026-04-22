"""
Evolution logic for the Prisoner's Dilemma tournament.

Supported update modes:
- replicator-like update
- threshold extinction
"""


def get_active_strategies(population):
    """
    Return strategy names with positive population.
    """
    return [name for name, size in population.items() if size > 0]


def get_average_fitness(scoreboard, population, ranking_key="average_score_per_effective_match"):
    """
    Compute population-weighted average fitness over active strategies.
    """
    total_population = sum(population.values())
    if total_population <= 0:
        return 0.0

    weighted_sum = 0.0
    for name, size in population.items():
        if size > 0:
            weighted_sum += size * scoreboard[name][ranking_key]

    return weighted_sum / total_population


def round_population_shares(raw_population, total_population):
    """
    Convert real-valued target populations into integer populations
    while preserving the total population size.
    """
    names = list(raw_population.keys())

    floored = {name: int(raw_population[name]) for name in names}
    remainder = total_population - sum(floored.values())

    fractional_parts = sorted(
        [(name, raw_population[name] - floored[name]) for name in names],
        key=lambda x: x[1],
        reverse=True
    )

    for i in range(remainder):
        floored[fractional_parts[i][0]] += 1

    return floored


def replicator_update(
    population,
    scoreboard,
    replicator_rate,
    ranking_key="average_score_per_effective_match"
):
    """
    Replicator-like update:
    - above-average strategies grow
    - below-average strategies shrink

    Formula idea:
        new_pop_i = pop_i * (1 + eta * (f_i - f_avg))

    Then clip at zero and renormalize to preserve total population.
    """
    total_population = sum(population.values())
    if total_population <= 0:
        return population.copy(), {
            "mode": "replicator",
            "average_fitness": 0.0,
            "note": "Total population is zero. No update applied."
        }

    average_fitness = get_average_fitness(
        scoreboard=scoreboard,
        population=population,
        ranking_key=ranking_key
    )

    raw_population = {}
    for name, old_pop in population.items():
        if old_pop <= 0:
            raw_population[name] = 0.0
            continue

        fitness = scoreboard[name][ranking_key]
        growth_factor = 1.0 + replicator_rate * (fitness - average_fitness)

        if growth_factor < 0:
            growth_factor = 0.0

        raw_population[name] = old_pop * growth_factor

    raw_total = sum(raw_population.values())

    if raw_total <= 0:
        return population.copy(), {
            "mode": "replicator",
            "average_fitness": average_fitness,
            "note": "All populations collapsed to zero under raw update. No update applied."
        }

    scaled_population = {}
    for name in raw_population:
        scaled_population[name] = raw_population[name] * total_population / raw_total

    new_population = round_population_shares(scaled_population, total_population)

    changes = {
        name: new_population[name] - population[name]
        for name in population
    }

    return new_population, {
        "mode": "replicator",
        "average_fitness": average_fitness,
        "changes": changes,
        "note": ""
    }


def threshold_extinction_update(
    population,
    scoreboard,
    extinction_threshold,
    redistribute=True,
    ranking_key="average_score_per_effective_match"
):
    """
    Threshold extinction:
    - strategies with fitness below threshold disappear completely
    - extinct population is redistributed among survivors in proportion
      to their fitness, if redistribute=True
    """
    total_population = sum(population.values())
    if total_population <= 0:
        return population.copy(), {
            "mode": "threshold_extinction",
            "extinct": [],
            "survivors": [],
            "note": "Total population is zero. No update applied."
        }

    active_names = get_active_strategies(population)

    extinct = []
    survivors = []

    for name in active_names:
        fitness = scoreboard[name][ranking_key]
        if fitness < extinction_threshold:
            extinct.append(name)
        else:
            survivors.append(name)

    # If nobody goes extinct, return unchanged.
    if not extinct:
        return population.copy(), {
            "mode": "threshold_extinction",
            "extinct": [],
            "survivors": survivors,
            "note": "No strategy fell below the extinction threshold."
        }

    # If everybody would go extinct, keep the old population.
    if not survivors:
        return population.copy(), {
            "mode": "threshold_extinction",
            "extinct": extinct,
            "survivors": [],
            "note": "All active strategies fell below threshold. No extinction applied."
        }

    extinct_population = sum(population[name] for name in extinct)

    new_population = population.copy()
    for name in extinct:
        new_population[name] = 0

    if redistribute and extinct_population > 0:
        survivor_weights = []
        for name in survivors:
            fitness = scoreboard[name][ranking_key]
            weight = max(fitness, 0.0)
            survivor_weights.append((name, weight))

        total_weight = sum(weight for _, weight in survivor_weights)

        if total_weight <= 0:
            # Fall back to equal redistribution
            equal_share = extinct_population / len(survivors)
            raw_additions = {name: equal_share for name in survivors}
        else:
            raw_additions = {
                name: extinct_population * weight / total_weight
                for name, weight in survivor_weights
            }

        floored = {name: int(raw_additions[name]) for name in survivors}
        assigned = sum(floored.values())
        remainder = extinct_population - assigned

        fractional_parts = sorted(
            [(name, raw_additions[name] - floored[name]) for name in survivors],
            key=lambda x: x[1],
            reverse=True
        )

        for i in range(remainder):
            floored[fractional_parts[i][0]] += 1

        for name in survivors:
            new_population[name] += floored[name]

    changes = {
        name: new_population[name] - population[name]
        for name in population
    }

    return new_population, {
        "mode": "threshold_extinction",
        "extinct": extinct,
        "survivors": survivors,
        "changes": changes,
        "note": ""
    }


def evolutionary_step(
    population,
    scoreboard,
    mode,
    replicator_rate=0.20,
    extinction_threshold=2.0,
    redistribute_extinct_population=True,
    ranking_key="average_score_per_effective_match"
):
    """
    Dispatch to the chosen evolutionary update rule.
    """
    if mode == "replicator":
        return replicator_update(
            population=population,
            scoreboard=scoreboard,
            replicator_rate=replicator_rate,
            ranking_key=ranking_key,
        )

    if mode == "threshold_extinction":
        return threshold_extinction_update(
            population=population,
            scoreboard=scoreboard,
            extinction_threshold=extinction_threshold,
            redistribute=redistribute_extinct_population,
            ranking_key=ranking_key,
        )

    raise ValueError(f"Unknown evolution mode: {mode}")