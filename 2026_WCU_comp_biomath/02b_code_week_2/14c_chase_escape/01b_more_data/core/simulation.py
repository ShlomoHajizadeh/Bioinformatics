"""
Main simulation engine
"""

import random

from .lattice import (
    create_lattice,
    place_agent,
    move_agent,
    TARGET,
    CHASER,
)
from .agents import Target, Chaser
from .movement import decide_target_move, decide_chaser_move
from .capture import apply_capture
from .utils import (
    set_random_seed,
    count_alive_targets,
    validate_positions,
    validate_unique_positions,
)
from analysis.reporter import SimulationReporter


class Simulation:
    def __init__(self, config):
        self.cfg = config

        set_random_seed(config.RANDOM_SEED)

        self.grid = create_lattice(config.LX, config.LY)

        self.targets = {}
        self.chasers = {}

        self.history_targets = []
        self.history_grids = []

        self.reporter = SimulationReporter()

        self._initialize_agents()
        self._store_history()

    def _random_empty_site(self):
        """
        Return a random empty lattice site.
        """
        while True:
            x = random.randint(0, self.cfg.LX - 1)
            y = random.randint(0, self.cfg.LY - 1)
            if self.grid[x, y] == 0:
                return x, y

    def _initialize_agents(self):
        """
        Randomly place targets and chasers on empty sites.
        """
        for i in range(self.cfg.N_TARGETS):
            x, y = self._random_empty_site()
            self.targets[i] = Target(i, x, y)
            place_agent(self.grid, x, y, TARGET)

        for i in range(self.cfg.N_CHASERS):
            x, y = self._random_empty_site()
            self.chasers[i] = Chaser(i, x, y)
            place_agent(self.grid, x, y, CHASER)

    def _store_history(self):
        """
        Store current observables and a copy of the grid.
        """
        alive_targets = count_alive_targets(self.targets)
        self.history_targets.append(alive_targets)
        self.history_grids.append(self.grid.copy())

    def validate_state(self):
        """
        Basic consistency checks for debugging.
        """
        validate_positions(self.targets, self.cfg.LX, self.cfg.LY)
        validate_positions(self.chasers, self.cfg.LX, self.cfg.LY)

        validate_unique_positions(
            {k: v for k, v in self.targets.items() if v.alive},
            self.chasers,
        )

        for target in self.targets.values():
            if target.alive:
                assert self.grid[target.x, target.y] == TARGET, (
                    f"Grid mismatch for target {target.id} at {(target.x, target.y)}"
                )

        for chaser in self.chasers.values():
            assert self.grid[chaser.x, chaser.y] == CHASER, (
                f"Grid mismatch for chaser {chaser.id} at {(chaser.x, chaser.y)}"
            )

    def step(self, t):
        """
        Perform one simulation step:
        1. Move targets in random order
        2. Move chasers in random order
        3. Apply captures immediately
        4. Record statistics
        """
        captures_this_step = 0

        # --------------------------------------------
        # Targets move in random order
        # --------------------------------------------
        target_ids = list(self.targets.keys())
        random.shuffle(target_ids)

        for target_id in target_ids:
            target = self.targets[target_id]

            if not target.alive:
                continue

            new_x, new_y = decide_target_move(
                target,
                self.chasers,
                self.grid,
                self.cfg.LX,
                self.cfg.LY,
            )

            moved = move_agent(self.grid, target.x, target.y, new_x, new_y, TARGET)
            if moved:
                target.x, target.y = new_x, new_y

        # --------------------------------------------
        # Chasers move in random order
        # --------------------------------------------
        chaser_ids = list(self.chasers.keys())
        random.shuffle(chaser_ids)

        for chaser_id in chaser_ids:
            chaser = self.chasers[chaser_id]

            action = decide_chaser_move(
                chaser,
                self.targets,
                self.grid,
                self.cfg.LX,
                self.cfg.LY,
            )

            old_x, old_y = chaser.x, chaser.y

            if action["type"] == "move":
                moved = move_agent(
                    self.grid,
                    old_x,
                    old_y,
                    action["new_x"],
                    action["new_y"],
                    CHASER,
                )
                if moved:
                    chaser.x = action["new_x"]
                    chaser.y = action["new_y"]

            elif action["type"] == "capture":
                target_id = action["target_id"]
                target = self.targets[target_id]

                if target.alive:
                    apply_capture(
                        chaser=chaser,
                        target=target,
                        grid=self.grid,
                        old_x=old_x,
                        old_y=old_y,
                        new_x=action["new_x"],
                        new_y=action["new_y"],
                        CHASER=CHASER,
                    )
                    captures_this_step += 1

        # --------------------------------------------
        # Record statistics
        # --------------------------------------------
        alive_targets = count_alive_targets(self.targets)
        self.history_targets.append(alive_targets)
        self.history_grids.append(self.grid.copy())

        self.reporter.record(t, self.targets, captures_this_step)

        if self.cfg.DEBUG:
            print(
                f"Step {t}: "
                f"targets alive = {alive_targets}, "
                f"captures this step = {captures_this_step}"
            )
            self.validate_state()

    def run(self):
        """
        Run the simulation for the configured number of steps.
        Stop early if all targets are captured.
        """
        for t in range(self.cfg.N_STEPS):
            self.step(t)

            if count_alive_targets(self.targets) == 0:
                if self.cfg.DEBUG:
                    print(f"All targets captured at step {t}.")
                break

        self.reporter.print_summary()