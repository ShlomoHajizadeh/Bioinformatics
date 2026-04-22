"""
Reporting utilities for the Prisoner's Dilemma evolutionary tournament.
"""

import csv
import os


class EvolutionReporter:
    """
    Collects and exports data from an evolutionary tournament run.
    """

    def __init__(self):
        self.history = []

    def record_generation(self, generation, population, scoreboard, update_info=None):
        """
        Store all relevant information for one generation.

        Parameters
        ----------
        generation : int
            Current generation number.
        population : dict
            Strategy name -> population size.
        scoreboard : dict
            Strategy name -> performance data.
        update_info : dict or None
            Information about the evolutionary replacement step.
        """
        entry = {
            "generation": generation,
            "population": population.copy(),
            "scoreboard": {name: data.copy() for name, data in scoreboard.items()},
            "update_info": update_info.copy() if update_info else None,
        }
        self.history.append(entry)

    def print_generation_summary(self, generation, population, scoreboard, update_info=None):
        """
        Print a compact summary for one generation.
        """
        print("\n" + "-" * 60)
        print(f"Generation {generation}")
        print("-" * 60)

        print("Population:")
        for name, size in population.items():
            print(f"  {name:18s}: {size}")

        print("\nPerformance:")
        ranking = sorted(
            scoreboard.items(),
            key=lambda item: item[1]["average_score_per_effective_match"],
            reverse=True
        )

        for pos, (name, data) in enumerate(ranking, start=1):
            print(
                f"  {pos:2d}. {name:18s} | "
                f"avg/effective match = {data['average_score_per_effective_match']:.3f} | "
                f"total score = {data['total_score']:.0f}"
            )

        if update_info is not None:
            print("\nEvolution step:")
            print(f"  strongest = {update_info['strongest']}")
            print(f"  weakest   = {update_info['weakest']}")
            print(f"  moved     = {update_info['moved']}")
            if update_info.get("note"):
                print(f"  note      = {update_info['note']}")

    def save_population_csv(self, filepath):
        """
        Save population history to a CSV file.

        One row per generation, one column per strategy.
        """
        if not self.history:
            print("No history recorded. Nothing to save.")
            return

        strategy_names = list(self.history[0]["population"].keys())

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["generation"] + strategy_names
            writer.writerow(header)

            for entry in self.history:
                row = [entry["generation"]]
                for name in strategy_names:
                    row.append(entry["population"][name])
                writer.writerow(row)

        print(f"Saved population history to: {filepath}")

    def save_score_csv(self, filepath):
        """
        Save average performance history to a CSV file.

        One row per generation, one column per strategy.
        """
        if not self.history:
            print("No history recorded. Nothing to save.")
            return

        strategy_names = list(self.history[0]["scoreboard"].keys())

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["generation"] + strategy_names
            writer.writerow(header)

            for entry in self.history:
                row = [entry["generation"]]
                for name in strategy_names:
                    value = entry["scoreboard"][name]["average_score_per_effective_match"]
                    row.append(value)
                writer.writerow(row)

        print(f"Saved score history to: {filepath}")

    def get_population_time_series(self):
        """
        Return population history in dictionary form.

        Returns
        -------
        dict
            strategy name -> list of population values
        """
        if not self.history:
            return {}

        strategy_names = list(self.history[0]["population"].keys())
        data = {name: [] for name in strategy_names}

        for entry in self.history:
            for name in strategy_names:
                data[name].append(entry["population"][name])

        return data

    def get_score_time_series(self):
        """
        Return performance history in dictionary form.

        Returns
        -------
        dict
            strategy name -> list of average_score_per_effective_match values
        """
        if not self.history:
            return {}

        strategy_names = list(self.history[0]["scoreboard"].keys())
        data = {name: [] for name in strategy_names}

        for entry in self.history:
            for name in strategy_names:
                value = entry["scoreboard"][name]["average_score_per_effective_match"]
                data[name].append(value)

        return data