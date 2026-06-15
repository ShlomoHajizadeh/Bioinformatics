"""
Tournament logic for all pairwise strategy encounters,
including population-weighted scoring.
"""

from core.game import play_match


def active_strategy_names(population):
    """
    Return the names of strategies with positive population.
    """
    return [name for name, size in population.items() if size > 0]


def run_population_tournament(
    strategies,
    population,
    rounds_per_match,
    include_self_play=True
):
    """
    Run a population-weighted round-robin tournament.

    Parameters
    ----------
    strategies : list
        List of strategy objects.
    population : dict
        Strategy name -> population size.
    rounds_per_match : int
        Number of rounds per match.
    include_self_play : bool
        If True, strategies also play against themselves.

    Returns
    -------
    results : list[dict]
        One entry per strategy pairing.
    scoreboard : dict
        Aggregated scores for each strategy.
    """
    active_strategies = [s for s in strategies if population.get(s.name, 0) > 0]

    scoreboard = {}
    for strategy in strategies:
        pop_size = population.get(strategy.name, 0)
        scoreboard[strategy.name] = {
            "population": pop_size,
            "total_score": 0,
            "effective_matches": 0,
            "average_score_per_effective_match": 0.0,
            "average_score_per_individual": 0.0,
        }

    results = []
    n = len(active_strategies)

    for i in range(n):
        j_start = i if include_self_play else i + 1

        for j in range(j_start, n):
            strategy_a = active_strategies[i]
            strategy_b = active_strategies[j]

            pop_a = population[strategy_a.name]
            pop_b = population[strategy_b.name]

            match_result = play_match(strategy_a, strategy_b, rounds_per_match)

            if strategy_a.name == strategy_b.name:
                weight = pop_a * pop_a
            else:
                weight = pop_a * pop_b

            weighted_score_a = match_result["score_a"] * weight
            weighted_score_b = match_result["score_b"] * weight

            scoreboard[strategy_a.name]["total_score"] += weighted_score_a
            scoreboard[strategy_a.name]["effective_matches"] += weight

            scoreboard[strategy_b.name]["total_score"] += weighted_score_b
            scoreboard[strategy_b.name]["effective_matches"] += weight

            results.append({
                "strategy_a": strategy_a.name,
                "strategy_b": strategy_b.name,
                "population_a": pop_a,
                "population_b": pop_b,
                "match_score_a": match_result["score_a"],
                "match_score_b": match_result["score_b"],
                "weight": weight,
                "weighted_score_a": weighted_score_a,
                "weighted_score_b": weighted_score_b,
            })

    for name, data in scoreboard.items():
        if data["effective_matches"] > 0:
            data["average_score_per_effective_match"] = (
                data["total_score"] / data["effective_matches"]
            )
        else:
            data["average_score_per_effective_match"] = 0.0

        if data["population"] > 0:
            data["average_score_per_individual"] = (
                data["total_score"] / data["population"]
            )
        else:
            data["average_score_per_individual"] = 0.0

    return results, scoreboard


def ranking_from_scoreboard(scoreboard, key="average_score_per_effective_match"):
    """
    Return strategies ranked descending by a chosen key.
    """
    return sorted(
        scoreboard.items(),
        key=lambda item: item[1][key],
        reverse=True
    )