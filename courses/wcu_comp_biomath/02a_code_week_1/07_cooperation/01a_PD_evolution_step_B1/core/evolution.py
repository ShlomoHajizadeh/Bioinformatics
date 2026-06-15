"""
Evolution logic:
weakest loses population, strongest gains population.
"""


def find_strongest_and_weakest(scoreboard, population, ranking_key="average_score_per_effective_match"):
    """
    Find the strongest and weakest active strategies.

    Only strategies with positive population are considered.
    """
    active_items = [
        (name, data)
        for name, data in scoreboard.items()
        if population.get(name, 0) > 0
    ]

    if not active_items:
        raise ValueError("No active strategies found.")

    strongest = max(active_items, key=lambda item: item[1][ranking_key])[0]
    weakest = min(active_items, key=lambda item: item[1][ranking_key])[0]

    return strongest, weakest


def evolutionary_step(population, scoreboard, transfer_amount, ranking_key="average_score_per_effective_match"):
    """
    Move population from weakest strategy to strongest strategy.

    Parameters
    ----------
    population : dict
        Current population sizes.
    scoreboard : dict
        Tournament results.
    transfer_amount : int
        Number of individuals to move.
    ranking_key : str
        Performance measure used for ranking.

    Returns
    -------
    new_population : dict
        Updated population.
    info : dict
        Summary of the update.
    """
    new_population = population.copy()

    strongest, weakest = find_strongest_and_weakest(
        scoreboard=scoreboard,
        population=population,
        ranking_key=ranking_key
    )

    if strongest == weakest:
        return new_population, {
            "strongest": strongest,
            "weakest": weakest,
            "moved": 0,
            "note": "No change because strongest and weakest are identical."
        }

    available = new_population[weakest]
    moved = min(transfer_amount, available)

    new_population[weakest] -= moved
    new_population[strongest] += moved

    return new_population, {
        "strongest": strongest,
        "weakest": weakest,
        "moved": moved,
        "note": ""
    }
