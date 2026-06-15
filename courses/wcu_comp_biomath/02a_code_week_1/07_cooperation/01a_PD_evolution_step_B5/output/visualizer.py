"""
Visualization utilities for the Prisoner's Dilemma evolutionary tournament.
"""

import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def plot_population_history(reporter, filepath=None, show=True):
    """
    Plot population trajectories over generations.
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
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        plt.savefig(filepath, dpi=150)
        print(f"Saved population plot to: {filepath}")

    if show:
        plt.show()
    else:
        plt.close()


def plot_score_history(reporter, filepath=None, show=True):
    """
    Plot average performance trajectories over generations.
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
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        plt.savefig(filepath, dpi=150)
        print(f"Saved score plot to: {filepath}")

    if show:
        plt.show()
    else:
        plt.close()


def plot_population_share_stacked(reporter, filepath=None, show=True):
    """
    Create a stacked area plot of population shares over generations.
    """
    data = reporter.get_population_time_series()
    if not data:
        print("No population history available for stacked area plot.")
        return

    strategy_names = list(data.keys())
    num_generations = len(next(iter(data.values())))
    generations = list(range(1, num_generations + 1))

    totals = []
    for i in range(num_generations):
        total_i = sum(data[name][i] for name in strategy_names)
        totals.append(total_i)

    shares = []
    for name in strategy_names:
        share_values = []
        for i in range(num_generations):
            if totals[i] > 0:
                share_values.append(data[name][i] / totals[i])
            else:
                share_values.append(0.0)
        shares.append(share_values)

    plt.figure(figsize=(10, 6))
    plt.stackplot(generations, *shares, labels=strategy_names)
    plt.xlabel("Generation")
    plt.ylabel("Population Share")
    plt.title("Population Shares Over Generations")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.tight_layout()

    if filepath is not None:
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        plt.savefig(filepath, dpi=150)
        print(f"Saved stacked population share plot to: {filepath}")

    if show:
        plt.show()
    else:
        plt.close()


def plot_population_bars_by_generation(reporter, output_dir=None, show=False):
    """
    Create one bar chart per generation.

    Parameters
    ----------
    reporter : EvolutionReporter
        Reporter containing simulation history.
    output_dir : str or None
        If given, save one PNG file per generation into this directory.
    show : bool
        If True, display each plot as it is created.
    """
    if not reporter.history:
        print("No history available for generation bar charts.")
        return

    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)

    for entry in reporter.history:
        generation = entry["generation"]
        population = entry["population"]

        names = list(population.keys())
        values = [population[name] for name in names]

        plt.figure(figsize=(10, 6))
        plt.bar(names, values)
        plt.xlabel("Strategy")
        plt.ylabel("Population")
        plt.title(f"Population by Strategy - Generation {generation}")
        plt.xticks(rotation=30, ha="right")
        plt.grid(True, axis="y")
        plt.tight_layout()

        if output_dir is not None:
            filepath = os.path.join(output_dir, f"population_gen_{generation:03d}.png")
            plt.savefig(filepath, dpi=150)
            print(f"Saved bar chart for generation {generation} to: {filepath}")

        if show:
            plt.show()
        else:
            plt.close()


def create_population_animation_gif(reporter, filepath, fps=1):
    """
    Create a GIF animation of population changes over time.

    Parameters
    ----------
    reporter : EvolutionReporter
        Reporter containing simulation history.
    filepath : str
        Output path for the GIF file.
    fps : int
        Frames per second in the GIF.
    """
    if not reporter.history:
        print("No history available for GIF animation.")
        return

    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    strategy_names = list(reporter.history[0]["population"].keys())
    max_population = 0

    for entry in reporter.history:
        generation_max = max(entry["population"].values())
        if generation_max > max_population:
            max_population = generation_max

    fig, ax = plt.subplots(figsize=(10, 6))

    def update(frame_index):
        ax.clear()

        entry = reporter.history[frame_index]
        generation = entry["generation"]
        population = entry["population"]

        names = strategy_names
        values = [population[name] for name in names]

        ax.bar(names, values)
        ax.set_xlabel("Strategy")
        ax.set_ylabel("Population")
        ax.set_title(f"Population Dynamics - Generation {generation}")
        ax.set_ylim(0, max_population * 1.1 if max_population > 0 else 1)
        ax.tick_params(axis="x", rotation=30)
        ax.grid(True, axis="y")

        for i, value in enumerate(values):
            ax.text(i, value + 0.2, str(value), ha="center", va="bottom")

        plt.tight_layout()

    animation = FuncAnimation(
        fig,
        update,
        frames=len(reporter.history),
        repeat=True
    )

    writer = PillowWriter(fps=fps)
    animation.save(filepath, writer=writer)
    plt.close(fig)

    print(f"Saved GIF animation to: {filepath}")