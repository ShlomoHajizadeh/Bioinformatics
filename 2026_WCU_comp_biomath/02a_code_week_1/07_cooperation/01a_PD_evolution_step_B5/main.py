"""
Main program for evolutionary Prisoner's Dilemma tournaments.

Phase 4:
Noisy interactions with additional forgiving strategies.
"""

import random

from config.config import (
    ROUNDS_PER_MATCH,
    INCLUDE_SELF_PLAY,
    RANDOM_SEED,
    GENERATIONS,
    INITIAL_POPULATION,
    EVOLUTION_MODE,
    REPLICATOR_RATE,
    EXTINCTION_THRESHOLD,
    REDISTRIBUTE_EXTINCT_POPULATION,
    PAYOFF_NAME,
    R,
    T,
    P,
    S,
    NOISE_ENABLED,
    ACTION_FLIP_PROBABILITY,
    GENEROUS_TIT_FOR_TAT_FORGIVENESS_PROBABILITY,
    FORGIVER_PUNISHMENT_LENGTH,
)

from core.tournament import run_population_tournament
from core.evolution import evolutionary_step

from output.reporter import EvolutionReporter
from output.visualizer import (
    plot_population_history,
    plot_score_history,
    plot_population_share_stacked,
    plot_population_bars_by_generation,
    create_population_animation_gif,
)

from strategies.always_cooperate import AlwaysCooperate
from strategies.always_defect import AlwaysDefect
from strategies.tit_for_tat import TitForTat
from strategies.random_strategy import RandomStrategy
from strategies.grudger import Grudger
from strategies.generous_tit_for_tat import GenerousTitForTat
from strategies.tit_for_two_tats import TitForTwoTats
from strategies.forgiver import Forgiver


def build_strategies():
    return [
        AlwaysCooperate(),
        AlwaysDefect(),
        TitForTat(),
        RandomStrategy(),
        Grudger(),
        GenerousTitForTat(
            forgiveness_probability=GENEROUS_TIT_FOR_TAT_FORGIVENESS_PROBABILITY
        ),
        TitForTwoTats(),
        Forgiver(
            punishment_length=FORGIVER_PUNISHMENT_LENGTH
        ),
    ]


def print_final_population(population):
    print("\n" + "=" * 60)
    print("FINAL POPULATION AFTER LAST UPDATE")
    print("=" * 60)
    for name, size in population.items():
        print(f"  {name:20s}: {size}")


def print_update_info(update_info):
    print("\nEvolution step:")
    print(f"  mode = {update_info.get('mode', '')}")

    if update_info["mode"] == "replicator":
        print(f"  average fitness = {update_info.get('average_fitness', 0.0):.3f}")
        changes = update_info.get("changes", {})
        if changes:
            print("  population changes:")
            for name, delta in changes.items():
                print(f"    {name:20s}: {delta:+d}")

    elif update_info["mode"] == "threshold_extinction":
        extinct = update_info.get("extinct", [])
        survivors = update_info.get("survivors", [])
        print(f"  extinct strategies = {extinct}")
        print(f"  surviving strategies = {survivors}")
        changes = update_info.get("changes", {})
        if changes:
            print("  population changes:")
            for name, delta in changes.items():
                print(f"    {name:20s}: {delta:+d}")

    note = update_info.get("note", "")
    if note:
        print(f"  note = {note}")


def main():
    random.seed(RANDOM_SEED)

    strategies = build_strategies()
    population = INITIAL_POPULATION.copy()
    reporter = EvolutionReporter()

    print("Evolutionary Prisoner's Dilemma Tournament")
    print(f"Payoff regime: {PAYOFF_NAME}")
    print(f"Payoffs: R={R}, T={T}, P={P}, S={S}")
    print(f"Noise enabled: {NOISE_ENABLED}")
    print(f"Action flip probability: {ACTION_FLIP_PROBABILITY}")
    print(f"Rounds per match: {ROUNDS_PER_MATCH}")
    print(f"Generations: {GENERATIONS}")
    print(f"Include self-play: {INCLUDE_SELF_PLAY}")
    print(f"Evolution mode: {EVOLUTION_MODE}")
    print(f"Strategies: {[s.name for s in strategies]}")

    if EVOLUTION_MODE == "replicator":
        print(f"Replicator rate: {REPLICATOR_RATE}")
    elif EVOLUTION_MODE == "threshold_extinction":
        print(f"Extinction threshold: {EXTINCTION_THRESHOLD}")
        print(f"Redistribute extinct population: {REDISTRIBUTE_EXTINCT_POPULATION}")

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
            mode=EVOLUTION_MODE,
            replicator_rate=REPLICATOR_RATE,
            extinction_threshold=EXTINCTION_THRESHOLD,
            redistribute_extinct_population=REDISTRIBUTE_EXTINCT_POPULATION,
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
            update_info=None,
        )

        print_update_info(update_info)

    print_final_population(population)

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

    plot_population_share_stacked(
        reporter,
        filepath="output/population_share_stacked.png",
        show=True,
    )

    plot_population_bars_by_generation(
        reporter,
        output_dir="output/bar_charts",
        show=False,
    )

    create_population_animation_gif(
        reporter,
        filepath="output/population_animation.gif",
        fps=1,
    )


if __name__ == "__main__":
    main()