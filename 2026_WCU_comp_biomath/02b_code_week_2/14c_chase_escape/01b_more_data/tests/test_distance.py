import math

from core.agents import Target, Chaser
from core.distance import (
    toroidal_dx,
    toroidal_dy,
    toroidal_distance,
    find_nearest_target,
    find_nearest_chaser,
)


def test_toroidal_dx_wrap():
    assert toroidal_dx(0, 9, 10) == 1
    assert toroidal_dx(2, 7, 10) == 5
    assert toroidal_dx(1, 4, 10) == 3


def test_toroidal_dy_wrap():
    assert toroidal_dy(0, 9, 10) == 1
    assert toroidal_dy(3, 8, 10) == 5
    assert toroidal_dy(2, 5, 10) == 3


def test_toroidal_distance_basic():
    d = toroidal_distance(0, 0, 9, 0, 10, 10)
    assert math.isclose(d, 1.0)


def test_find_nearest_target():
    chaser = Chaser(id=0, x=0, y=0)
    targets = {
        0: Target(id=0, x=2, y=0),
        1: Target(id=1, x=5, y=5),
    }

    nearest, dist = find_nearest_target(chaser, targets, 10, 10)

    assert len(nearest) == 1
    assert nearest[0].id == 0
    assert math.isclose(dist, 2.0)


def test_find_nearest_chaser():
    target = Target(id=0, x=0, y=0)
    chasers = {
        0: Chaser(id=0, x=2, y=0),
        1: Chaser(id=1, x=5, y=5),
    }

    nearest, dist = find_nearest_chaser(target, chasers, 10, 10)

    assert len(nearest) == 1
    assert nearest[0].id == 0
    assert math.isclose(dist, 2.0)