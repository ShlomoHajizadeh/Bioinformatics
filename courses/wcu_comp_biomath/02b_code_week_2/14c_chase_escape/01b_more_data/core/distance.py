"""
Toroidal distance computations
"""

import numpy as np


def toroidal_dx(x1, x2, LX):
    dx = abs(x1 - x2)
    return min(dx, LX - dx)


def toroidal_dy(y1, y2, LY):
    dy = abs(y1 - y2)
    return min(dy, LY - dy)


def toroidal_distance(x1, y1, x2, y2, LX, LY):
    dx = toroidal_dx(x1, x2, LX)
    dy = toroidal_dy(y1, y2, LY)
    return np.sqrt(dx * dx + dy * dy)


def find_nearest_target(chaser, targets, LX, LY):
    min_dist = float("inf")
    nearest = []

    for t in targets.values():
        if not t.alive:
            continue

        d = toroidal_distance(chaser.x, chaser.y, t.x, t.y, LX, LY)

        if d < min_dist:
            min_dist = d
            nearest = [t]
        elif d == min_dist:
            nearest.append(t)

    return nearest, min_dist


def find_nearest_chaser(target, chasers, LX, LY):
    min_dist = float("inf")
    nearest = []

    for c in chasers.values():
        d = toroidal_distance(target.x, target.y, c.x, c.y, LX, LY)

        if d < min_dist:
            min_dist = d
            nearest = [c]
        elif d == min_dist:
            nearest.append(c)

    return nearest, min_dist