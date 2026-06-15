"""
Visualization utilities for the Prisoner's Dilemma evolutionary tournament.
"""

import os
import matplotlib.pyplot as plt


def plot_population_history(reporter, filepath=None, show=True):
    """
    Plot population trajectories over generations.

    Parameters
    ----------
    reporter : EvolutionReporter
        Reporter containing simulation history.
    filepath : str or None
        If given, save the figure to this file.
    show : bool
        If True, display the plot.
    """
    data = reporter.get_population_time_series()
    if not data:
        print("No population history available for plotting.")
        return

    num_generations = len(next(iter(data.values())))
    generations = list(range(1, num_generations + 1))

    plt.figure(figsize=(10, 6))
    for strategy_name, values in data.items():
        plt.plot(generations, values, marker="o", label=strategy_name)

    plt.xlabel("Generation")
    plt.ylabel("Population")
    plt.title("Population Trajectories of Strategies")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if filepath is not None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=150)
        print(f"Saved population plot to: {filepath}")

    if show:
        plt.show()
    else:
        plt.close()


def plot_score_history(reporter, filepath=None, show=True):
    """
    Plot average performance trajectories over generations.

    Parameters
    ----------
    reporter : EvolutionReporter
        Reporter containing simulation history.
    filepath : str or None
        If given, save the figure to this file.
    show : bool
        If True, display the plot.
    """
    data = reporter.get_score_time_series()
    if not data:
        print("No score history available for plotting.")
        return

    num_generations = len(next(iter(data.values())))
    generations = list(range(1, num_generations + 1))

    plt.figure(figsize=(10, 6))
    for strategy_name, values in data.items():
        plt.plot(generations, values, marker="o", label=strategy_name)

    plt.xlabel("Generation")
    plt.ylabel("Average Score per Effective Match")
    plt.title("Performance Trajectories of Strategies")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if filepath is not None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=150)
        print(f"Saved score plot to: {filepath}")

    if show:
        plt.show()
    else:
        plt.close()