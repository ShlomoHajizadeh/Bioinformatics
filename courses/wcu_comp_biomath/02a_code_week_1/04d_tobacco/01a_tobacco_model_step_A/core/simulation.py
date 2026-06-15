"""
Simulation class for Version A.
"""

import numpy as np

from core.grid import (
    initialize_plant_health,
    initialize_egg_queues,
    initialize_caterpillars,
    random_positions,
)
from core.interactions import step_version_a


class Simulation:
    def __init__(self, params):
        self.params = params
        self.rng = np.random.default_rng(params.RANDOM_SEED)

        self.state = {
            "step": 0,
            "phase": "day",
            "rng": self.rng,
            "plant_health": initialize_plant_health(
                params.GRID_HEIGHT,
                params.GRID_WIDTH,
                params.INITIAL_PLANT_HEALTH,
            ),
            "eggs_queue": initialize_egg_queues(
                params.GRID_HEIGHT,
                params.GRID_WIDTH,
                params.EGG_HATCH_DELAY,
            ),
            "caterpillars": initialize_caterpillars(
                params.GRID_HEIGHT, params.GRID_WIDTH
            ),
            "moth_x": None,
            "moth_y": None,
            "pred_x": None,
            "pred_y": None,
            "predation": np.zeros((params.GRID_HEIGHT, params.GRID_WIDTH), dtype=int),
            "newly_laid_eggs": np.zeros((params.GRID_HEIGHT, params.GRID_WIDTH), dtype=int),
            "hatching": np.zeros((params.GRID_HEIGHT, params.GRID_WIDTH), dtype=int),
        }

        moth_x, moth_y = random_positions(
            params.N_MOTHS, params.GRID_HEIGHT, params.GRID_WIDTH, self.rng
        )
        pred_x, pred_y = random_positions(
            params.N_PREDATORS, params.GRID_HEIGHT, params.GRID_WIDTH, self.rng
        )

        self.state["moth_x"] = moth_x
        self.state["moth_y"] = moth_y
        self.state["pred_x"] = pred_x
        self.state["pred_y"] = pred_y

        self.history = {
            "step": [],
            "phase": [],
            "mean_plant_health": [],
            "total_eggs": [],
            "total_caterpillars": [],
            "total_predation": [],
        }

        self.frames = []

    def validate_state(self):
        plant_health = self.state["plant_health"]
        eggs_queue = self.state["eggs_queue"]
        caterpillars = self.state["caterpillars"]
        moth_x = self.state["moth_x"]
        moth_y = self.state["moth_y"]
        pred_x = self.state["pred_x"]
        pred_y = self.state["pred_y"]

        h, w = plant_health.shape

        assert eggs_queue.shape[1:] == (h, w), "Egg queue shape mismatch"
        assert caterpillars.shape == (h, w), "Caterpillar shape mismatch"
        assert np.all(np.isfinite(plant_health)), "Plant health has non-finite values"
        assert np.all((0.0 <= plant_health) & (plant_health <= self.params.PLANT_MAX_HEALTH)), \
            "Plant health outside valid range"
        assert np.all(caterpillars >= 0), "Negative caterpillar counts"
        assert np.all(eggs_queue >= 0), "Negative egg counts"
        assert np.all((0 <= moth_x) & (moth_x < w)), "Moth x positions out of range"
        assert np.all((0 <= moth_y) & (moth_y < h)), "Moth y positions out of range"
        assert np.all((0 <= pred_x) & (pred_x < w)), "Predator x positions out of range"
        assert np.all((0 <= pred_y) & (pred_y < h)), "Predator y positions out of range"

    def record_history(self):
        self.history["step"].append(self.state["step"])
        self.history["phase"].append(self.state["phase"])
        self.history["mean_plant_health"].append(self.state["plant_health"].mean())
        self.history["total_eggs"].append(int(self.state["eggs_queue"].sum()))
        self.history["total_caterpillars"].append(int(self.state["caterpillars"].sum()))
        self.history["total_predation"].append(int(self.state["predation"].sum()))

    def capture_frame(self):
        frame = {
            "step": self.state["step"],
            "phase": self.state["phase"],
            "plant_health": self.state["plant_health"].copy(),
            "caterpillars": self.state["caterpillars"].copy(),
            "moth_x": self.state["moth_x"].copy(),
            "moth_y": self.state["moth_y"].copy(),
            "pred_x": self.state["pred_x"].copy(),
            "pred_y": self.state["pred_y"].copy(),
        }
        self.frames.append(frame)

    def step(self):
        self.state = step_version_a(self.state, self.params)
        self.validate_state()
        self.record_history()

        if self.state["step"] % self.params.SNAPSHOT_EVERY == 0:
            self.capture_frame()

        if self.params.DEBUG and self.state["step"] % self.params.PRINT_EVERY == 0:
            print(
                f"Step {self.state['step']:4d} | "
                f"{self.state['phase']:5s} | "
                f"mean health = {self.state['plant_health'].mean():.3f} | "
                f"eggs = {int(self.state['eggs_queue'].sum()):4d} | "
                f"caterpillars = {int(self.state['caterpillars'].sum()):4d} | "
                f"predation = {int(self.state['predation'].sum()):4d}"
            )

    def run(self):
        self.capture_frame()
        for _ in range(self.params.N_STEPS):
            self.step()
        return self.history, self.frames