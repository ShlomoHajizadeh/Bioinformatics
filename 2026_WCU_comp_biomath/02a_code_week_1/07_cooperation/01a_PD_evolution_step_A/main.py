"""
Main program for Phase 1:
Baseline tournament without evolution.
"""

import random

from config.config import ROUNDS_PER_MATCH, INCLUDE_SELF_PLAY, RANDOM_SEED
from core.tournament import run_tournament, ranking_from_scoreboard

from strategies.always_cooperate import AlwaysCooperate
from strategies.always_defect import AlwaysDefect
from strategies.tit_for_tat import TitForTat
from strategies.random_strategy import RandomStrategy
from strategies.grudger import Grudger


def build_strategies():
    """
    Create one instance of each strategy.
    """
    return [
        AlwaysCooperate(),
        AlwaysDefect(),
        TitForTat(),
        RandomStrategy(),
        Grudger(),
    ]


def print_match_results(results):
    print("\n=== MATCH RESULTS ===")
    for result in results:
        print(
            f"{result['strategy_a']} vs {result['strategy_b']}: "
            f"{result['score_a']} - {result['score_b']}"
        )


def print_scoreboard(scoreboard):
    print("\n=== SCOREBOARD ===")
    for name, data in scoreboard.items():
        print(
            f"{name:18s} | "
            f"total = {data['total_score']:4d} | "
            f"avg/match = {data['average_score_per_match']:.2f} | "
            f"avg/round = {data['average_score_per_round']:.2f}"
        )


def print_ranking(scoreboard):
    print("\n=== RANKING ===")
    ranking = ranking_from_scoreboard(scoreboard)
    for position, (name, data) in enumerate(ranking, start=1):
        print(
            f"{position:2d}. {name:18s} "
            f"(total score = {data['total_score']})"
        )


def main():
    random.seed(RANDOM_SEED)

    strategies = build_strategies()

    results, scoreboard = run_tournament(
        strategies=strategies,
        rounds_per_match=ROUNDS_PER_MATCH,
        include_self_play=INCLUDE_SELF_PLAY,
    )

    print("Baseline Tournament: Iterated Prisoner's Dilemma")
    print(f"Rounds per match: {ROUNDS_PER_MATCH}")
    print(f"Include self-play: {INCLUDE_SELF_PLAY}")

    print_match_results(results)
    print_scoreboard(scoreboard)
    print_ranking(scoreboard)


if __name__ == "__main__":
    main()