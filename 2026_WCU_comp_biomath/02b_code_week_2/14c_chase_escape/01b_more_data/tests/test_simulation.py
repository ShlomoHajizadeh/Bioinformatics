from config.config import Config
from core.simulation import Simulation
from core.lattice import TARGET, CHASER


def test_simulation_initial_counts():
    cfg = Config(
        LX=20,
        LY=20,
        N_CHASERS=3,
        N_TARGETS=8,
        N_STEPS=5,
        RANDOM_SEED=123,
        DEBUG=False,
    )

    sim = Simulation(cfg)

    assert len(sim.targets) == 8
    assert len(sim.chasers) == 3
    assert sim.history_targets[0] == 8
    assert len(sim.history_grids) == 1


def test_simulation_run_history_lengths():
    cfg = Config(
        LX=20,
        LY=20,
        N_CHASERS=2,
        N_TARGETS=5,
        N_STEPS=4,
        RANDOM_SEED=123,
        DEBUG=False,
    )

    sim = Simulation(cfg)
    sim.run()

    assert len(sim.history_targets) >= 1
    assert len(sim.history_grids) == len(sim.history_targets)


def test_simulation_grid_contains_only_valid_codes():
    cfg = Config(
        LX=15,
        LY=15,
        N_CHASERS=2,
        N_TARGETS=4,
        N_STEPS=3,
        RANDOM_SEED=7,
        DEBUG=False,
    )

    sim = Simulation(cfg)
    sim.run()

    valid_codes = {0, TARGET, CHASER}
    assert set(sim.grid.flatten()).issubset(valid_codes)


def test_simulation_alive_targets_match_grid():
    cfg = Config(
        LX=20,
        LY=20,
        N_CHASERS=3,
        N_TARGETS=6,
        N_STEPS=5,
        RANDOM_SEED=5,
        DEBUG=False,
    )

    sim = Simulation(cfg)
    sim.run()

    alive_positions = {
        (target.x, target.y)
        for target in sim.targets.values()
        if target.alive
    }

    grid_target_positions = set(zip(*((sim.grid == TARGET).nonzero())))

    assert alive_positions == grid_target_positions