import random

from core.agents import Target, Chaser
from core.lattice import create_lattice, place_agent, TARGET, CHASER
from core.movement import decide_chaser_move


def test_chaser_moves_toward_target_on_empty_site():
    random.seed(1)

    LX, LY = 10, 10
    grid = create_lattice(LX, LY)

    chaser = Chaser(id=0, x=5, y=5)
    target = Target(id=0, x=5, y=7)

    place_agent(grid, chaser.x, chaser.y, CHASER)
    place_agent(grid, target.x, target.y, TARGET)

    targets = {0: target}

    action = decide_chaser_move(chaser, targets, grid, LX, LY)

    assert action["type"] in ["move", "capture"]
    assert (action["new_x"], action["new_y"]) in [(5, 6)]


def test_chaser_captures_when_target_is_best_neighbor():
    random.seed(1)

    LX, LY = 10, 10
    grid = create_lattice(LX, LY)

    chaser = Chaser(id=0, x=5, y=5)
    target = Target(id=0, x=5, y=6)

    place_agent(grid, chaser.x, chaser.y, CHASER)
    place_agent(grid, target.x, target.y, TARGET)

    targets = {0: target}

    action = decide_chaser_move(chaser, targets, grid, LX, LY)

    assert action["type"] == "capture"
    assert action["new_x"] == 5
    assert action["new_y"] == 6
    assert action["target_id"] == 0


def test_chaser_stays_if_best_site_is_blocked_by_non_target():
    random.seed(1)

    LX, LY = 10, 10
    grid = create_lattice(LX, LY)

    chaser = Chaser(id=0, x=5, y=5)
    target = Target(id=0, x=5, y=7)

    place_agent(grid, chaser.x, chaser.y, CHASER)
    place_agent(grid, target.x, target.y, TARGET)

    # Best step toward target is (5, 6), block it with another chaser marker
    place_agent(grid, 5, 6, CHASER)

    targets = {0: target}

    action = decide_chaser_move(chaser, targets, grid, LX, LY)

    assert action["type"] == "stay"
    assert action["new_x"] == 5
    assert action["new_y"] == 5