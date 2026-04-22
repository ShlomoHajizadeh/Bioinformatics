"""
Main entry point for Version C of the tobacco ecosystem model.
"""

import os

from config import config as params
from core.simulation import Simulation
from output.plots import (
    plot_time_series,
    plot_final_health,
    plot_final_defense,
    plot_final_signal,
)
from output.animation import create_animation


def main():
    os.makedirs(params.OUTPUT_DIR, exist_ok=True)

    sim = Simulation(params)
    history, frames = sim.run()

    plot_time_series(history, params.OUTPUT_DIR)
    plot_final_health(sim.state["plant_health"], params.OUTPUT_DIR)
    plot_final_defense(sim.state["defense_level"], params.OUTPUT_DIR)
    plot_final_signal(sim.state["signal"], params.OUTPUT_DIR)

    gif_path = create_animation(
        frames,
        params.OUTPUT_DIR,
        gif_name=params.GIF_NAME,
        interval=200,
    )

    print("\nSimulation finished.")
    print(f"Outputs saved in: {params.OUTPUT_DIR}")
    print(f"Animation saved as: {gif_path}")


if __name__ == "__main__":
    main()