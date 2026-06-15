import numpy as np
import random

from core.agents import Target, Chaser
from core.lattice import create_lattice, place_agent, TARGET, CHASER
from core.movement import decide_target_move


def test_target_moves_away_from_nearest_chaser():
    random.seed(1)

    LX, LY = 10, 10
    grid = create_lattice(LX, LY)

    target = Target(id=0, x=5, y=5)
    chaser = Chaser(id=0, x=5, y=4)

    place_agent(grid, target.x, target.y, TARGET)
    place_agent(grid, chaser.x, chaser.y, CHASER)

    chasers = {0: chaser}

    new_x, new_y = decide_target_move(target, chasers, grid, LX, LY)

    assert (new_x, new_y) in [(6, 5), (4, 5), (5, 6)]


def test_target_stays_if_best_choice_is_blocked():
    random.seed(0)

    LX, LY = 5, 5
    grid = create_lattice(LX, LY)

    target = Target(id=0, x=2, y=2)
    chaser = Chaser(id=0, x=2, y=1)

    place_agent(grid, 2, 2, TARGET)
    place_agent(grid, 2, 1, CHASER)

    # Block all positions that are farther away from the chaser
    place_agent(grid, 1, 2, CHASER)
    place_agent(grid, 3, 2, CHASER)
    place_agent(grid, 2, 3, CHASER)

    chasers = {
        0: chaser,
        1: Chaser(id=1, x=1, y=2),
        2: Chaser(id=2, x=3, y=2),
        3: Chaser(id=3, x=2, y=3),
    }

    new_x, new_y = decide_target_move(target, chasers, grid, LX, LY)

    assert (new_x, new_y) == (2, 2)