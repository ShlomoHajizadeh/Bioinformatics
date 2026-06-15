from core.agents import Target, Chaser
from core.lattice import create_lattice, place_agent, TARGET, CHASER
from core.capture import apply_capture


def test_apply_capture_moves_chaser_and_kills_target():
    LX, LY = 10, 10
    grid = create_lattice(LX, LY)

    chaser = Chaser(id=0, x=5, y=5)
    target = Target(id=0, x=5, y=6)

    place_agent(grid, chaser.x, chaser.y, CHASER)
    place_agent(grid, target.x, target.y, TARGET)

    apply_capture(
        chaser=chaser,
        target=target,
        grid=grid,
        old_x=5,
        old_y=5,
        new_x=5,
        new_y=6,
        CHASER=CHASER,
    )

    assert (chaser.x, chaser.y) == (5, 6)
    assert target.alive is False
    assert grid[5, 5] == 0
    assert grid[5, 6] == CHASER