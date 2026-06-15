"""
Tournament logic for all pairwise strategy encounters.
"""

from core.game import play_match


def run_tournament(strategies, rounds_per_match, include_self_play=True):
    """
    Run a round-robin tournament among all strategies.

    Parameters
    ----------
    strategies : list
        List of strategy objects.
    rounds_per_match : int
        Number of rounds in each repeated game.
    include_self_play : bool
        If True, strategies also play against themselves.

    Returns
    -------
    results : list[dict]
        Match-by-match results.
    scoreboard : dict
        Aggregated performance for each strategy.
    """
    results = []
    scoreboard = {}

    for strategy in strategies:
        scoreboard[strategy.name] = {
            "total_score": 0,
            "matches_played": 0,
            "rounds_played": 0,
        }

    n = len(strategies)

    for i in range(n):
        j_start = i if include_self_play else i + 1

        for j in range(j_start, n):
            strategy_a = strategies[i]
            strategy_b = strategies[j]

            match_result = play_match(strategy_a, strategy_b, rounds_per_match)
            results.append(match_result)

            scoreboard[strategy_a.name]["total_score"] += match_result["score_a"]
            scoreboard[strategy_a.name]["matches_played"] += 1
            scoreboard[strategy_a.name]["rounds_played"] += rounds_per_match

            scoreboard[strategy_b.name]["total_score"] += match_result["score_b"]
            scoreboard[strategy_b.name]["matches_played"] += 1
            scoreboard[strategy_b.name]["rounds_played"] += rounds_per_match

    for strategy_name, data in scoreboard.items():
        if data["matches_played"] > 0:
            data["average_score_per_match"] = data["total_score"] / data["matches_played"]
        else:
            data["average_score_per_match"] = 0.0

        if data["rounds_played"] > 0:
            data["average_score_per_round"] = data["total_score"] / data["rounds_played"]
        else:
            data["average_score_per_round"] = 0.0

    return results, scoreboard


def ranking_from_scoreboard(scoreboard):
    """
    Return a ranking sorted by total score descending.
    """
    return sorted(
        scoreboard.items(),
        key=lambda item: item[1]["total_score"],
        reverse=True
    )
