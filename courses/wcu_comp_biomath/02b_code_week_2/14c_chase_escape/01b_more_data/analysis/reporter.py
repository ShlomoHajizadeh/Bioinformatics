"""
Reporting utilities for the chase-and-escape simulation

This module collects, summarizes, and optionally prints or saves
simulation results.
"""

import numpy as np


class SimulationReporter:
    def __init__(self):
        self.time = []
        self.targets_alive = []
        self.captures = []

    def record(self, t, targets, captures_this_step):
        """
        Record simulation state at time t
        """
        alive = sum(tg.alive for tg in targets.values())

        self.time.append(t)
        self.targets_alive.append(alive)
        self.captures.append(captures_this_step)

    def summary(self):
        """
        Return key statistics of the simulation
        """
        if len(self.time) == 0:
            return {}

        total_captures = sum(self.captures)
        initial_targets = self.targets_alive[0]
        final_targets = self.targets_alive[-1]

        extinction_time = None
        for t, val in zip(self.time, self.targets_alive):
            if val == 0:
                extinction_time = t
                break

        return {
            "initial_targets": initial_targets,
            "final_targets": final_targets,
            "total_captures": total_captures,
            "extinction_time": extinction_time,
            "mean_captures_per_step": np.mean(self.captures),
        }

    def print_summary(self):
        """
        Pretty print summary statistics
        """
        stats = self.summary()

        if not stats:
            print("No data recorded.")
            return

        print("\n--- Simulation Summary ---")
        print(f"Initial targets:        {stats['initial_targets']}")
        print(f"Final targets:          {stats['final_targets']}")
        print(f"Total captures:         {stats['total_captures']}")
        print(f"Mean captures/step:     {stats['mean_captures_per_step']:.2f}")

        if stats["extinction_time"] is not None:
            print(f"Extinction time:        {stats['extinction_time']}")
        else:
            print("Extinction time:        Not reached")

    def to_dict(self):
        """
        Export all recorded data (useful for later extensions / saving)
        """
        return {
            "time": self.time,
            "targets_alive": self.targets_alive,
            "captures": self.captures,
        }