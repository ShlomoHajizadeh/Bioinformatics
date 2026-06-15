"""
Main program for Phase 2:
Evolutionary replacement over several generations.
"""

import random

from config.config import (
    ROUNDS_PER_MATCH,
    INCLUDE_SELF_PLAY,
    RANDOM_SEED,
    GENERATIONS,
    INITIAL_POPULATION,
    TRANSFER_AMOUNT,
)

from core.tournament import run_population_tournament
from core.evolution import evolutionary_step

from output.reporter import EvolutionReporter
from output.visualizer import plot_population_history, plot_score_history

from strategies.always_cooperate import AlwaysCooperate
from strategies.always_defect import AlwaysDefect
from strategies.tit_for_tat import TitForTat
from strategies.random_strategy import RandomStrategy
from strategies.grudger import Grudger


def build_strategies():
    return [
        AlwaysCooperate(),
        AlwaysDefect(),
        TitForTat(),
        RandomStrategy(),
        Grudger(),
    ]


def main():
    random.seed(RANDOM_SEED)

    strategies = build_strategies()
    population = INITIAL_POPULATION.copy()
    reporter = EvolutionReporter()

    print("Evolutionary Replacement Tournament")
    print(f"Rounds per match: {ROUNDS_PER_MATCH}")
    print(f"Generations: {GENERATIONS}")
    print(f"Transfer amount: {TRANSFER_AMOUNT}")
    print(f"Include self-play: {INCLUDE_SELF_PLAY}")

    for generation in range(1, GENERATIONS + 1):
        results, scoreboard = run_population_tournament(
            strategies=strategies,
            population=population,
            rounds_per_match=ROUNDS_PER_MATCH,
            include_self_play=INCLUDE_SELF_PLAY,
        )

        population_before_update = population.copy()

        population, update_info = evolutionary_step(
            population=population,
            scoreboard=scoreboard,
            transfer_amount=TRANSFER_AMOUNT,
        )

        reporter.record_generation(
            generation=generation,
            population=population_before_update,
            scoreboard=scoreboard,
            update_info=update_info,
        )

        reporter.print_generation_summary(
            generation=generation,
            population=population_before_update,
            scoreboard=scoreboard,
            update_info=update_info,
        )

    print("\n" + "=" * 60)
    print("FINAL POPULATION AFTER LAST UPDATE")
    print("=" * 60)
    for name, size in population.items():
        print(f"  {name:18s}: {size}")

    reporter.save_population_csv("output/population_history.csv")
    reporter.save_score_csv("output/score_history.csv")

    plot_population_history(
        reporter,
        filepath="output/population_history.png",
        show=True,
    )

    plot_score_history(
        reporter,
        filepath="output/score_history.png",
        show=True,
    )


if __name__ == "__main__":
    main()