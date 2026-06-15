"""
Simulation class for Version C.
"""

import numpy as np

from core.grid import (
    initialize_plant_health,
    initialize_attacked,
    initialize_defense_level,
    initialize_bloom_mode,
    initialize_signal,
    initialize_priming,
    initialize_egg_queues,
    initialize_caterpillars,
    random_positions,
)
from core.interactions import step_version_c


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
            "attacked": initialize_attacked(params.GRID_HEIGHT, params.GRID_WIDTH),
            "defense_level": initialize_defense_level(
                params.GRID_HEIGHT, params.GRID_WIDTH
            ),
            "bloom_mode": initialize_bloom_mode(
                params.GRID_HEIGHT, params.GRID_WIDTH, params.BLOOM_NIGHT
            ),
            "signal": initialize_signal(params.GRID_HEIGHT, params.GRID_WIDTH),
            "priming": initialize_priming(params.GRID_HEIGHT, params.GRID_WIDTH),
            "effective_threshold": np.full(
                (params.GRID_HEIGHT, params.GRID_WIDTH),
                float(params.DEFENSE_ON_THRESHOLD),
                dtype=float,
            ),
            "eggs_queue": initialize_egg_queues(
                params.GRID_HEIGHT, params.GRID_WIDTH, params.EGG_HATCH_DELAY
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
            "attacked_fraction": [],
            "mean_defense_level": [],
            "day_bloom_fraction": [],
            "mean_signal": [],
            "mean_priming": [],
            "mean_effective_threshold": [],
        }

        self.frames = []

    def validate_state(self):
        plant_health = self.state["plant_health"]
        attacked = self.state["attacked"]
        defense_level = self.state["defense_level"]
        bloom_mode = self.state["bloom_mode"]
        signal = self.state["signal"]
        priming = self.state["priming"]
        effective_threshold = self.state["effective_threshold"]
        eggs_queue = self.state["eggs_queue"]
        caterpillars = self.state["caterpillars"]
        moth_x = self.state["moth_x"]
        moth_y = self.state["moth_y"]
        pred_x = self.state["pred_x"]
        pred_y = self.state["pred_y"]

        h, w = plant_health.shape

        assert attacked.shape == (h, w), "Attacked shape mismatch"
        assert defense_level.shape == (h, w), "Defense shape mismatch"
        assert bloom_mode.shape == (h, w), "Bloom mode shape mismatch"
        assert signal.shape == (h, w), "Signal shape mismatch"
        assert priming.shape == (h, w), "Priming shape mismatch"
        assert effective_threshold.shape == (h, w), "Threshold shape mismatch"
        assert eggs_queue.shape[1:] == (h, w), "Egg queue shape mismatch"
        assert caterpillars.shape == (h, w), "Caterpillar shape mismatch"

        assert np.all(np.isfinite(plant_health)), "Plant health has non-finite values"
        assert np.all(np.isfinite(defense_level)), "Defense has non-finite values"
        assert np.all(np.isfinite(signal)), "Signal has non-finite values"
        assert np.all(np.isfinite(priming)), "Priming has non-finite values"

        assert np.all(
            (0.0 <= plant_health) & (plant_health <= self.params.PLANT_MAX_HEALTH)
        ), "Plant health outside valid range"
        assert np.all(
            (0.0 <= defense_level) & (defense_level <= self.params.DEFENSE_MAX)
        ), "Defense outside valid range"
        assert np.all(
            (0.0 <= signal) & (signal <= self.params.SIGNAL_MAX)
        ), "Signal outside valid range"
        assert np.all(
            (0.0 <= priming) & (priming <= self.params.PRIMING_MAX)
        ), "Priming outside valid range"

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
        self.history["attacked_fraction"].append(self.state["attacked"].mean())
        self.history["mean_defense_level"].append(self.state["defense_level"].mean())
        self.history["day_bloom_fraction"].append(
            (self.state["bloom_mode"] == self.params.BLOOM_DAY).mean()
        )
        self.history["mean_signal"].append(self.state["signal"].mean())
        self.history["mean_priming"].append(self.state["priming"].mean())
        self.history["mean_effective_threshold"].append(
            self.state["effective_threshold"].mean()
        )

    def capture_frame(self):
        frame = {
            "step": self.state["step"],
            "phase": self.state["phase"],
            "plant_health": self.state["plant_health"].copy(),
            "attacked": self.state["attacked"].copy(),
            "defense_level": self.state["defense_level"].copy(),
            "bloom_mode": self.state["bloom_mode"].copy(),
            "signal": self.state["signal"].copy(),
            "priming": self.state["priming"].copy(),
            "caterpillars": self.state["caterpillars"].copy(),
            "moth_x": self.state["moth_x"].copy(),
            "moth_y": self.state["moth_y"].copy(),
            "pred_x": self.state["pred_x"].copy(),
            "pred_y": self.state["pred_y"].copy(),
        }
        self.frames.append(frame)

    def step(self):
        self.state = step_version_c(self.state, self.params)
        self.validate_state()
        self.record_history()

        if self.state["step"] % self.params.SNAPSHOT_EVERY == 0:
            self.capture_frame()

        if self.params.DEBUG and self.state["step"] % self.params.PRINT_EVERY == 0:
            print(
                f"Step {self.state['step']:4d} | "
                f"{self.state['phase']:5s} | "
                f"mean health = {self.state['plant_health'].mean():.3f} | "
                f"caterpillars = {int(self.state['caterpillars'].sum()):4d} | "
                f"mean defense = {self.state['defense_level'].mean():.3f} | "
                f"mean signal = {self.state['signal'].mean():.3f} | "
                f"mean priming = {self.state['priming'].mean():.3f}"
            )

    def run(self):
        self.capture_frame()
        for _ in range(self.params.N_STEPS):
            self.step()
        return self.history, self.frames