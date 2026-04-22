"""
Lattice handling with toroidal boundary conditions
"""

import numpy as np


EMPTY = 0
TARGET = 1
CHASER = 2


def create_lattice(LX, LY):
    return np.zeros((LX, LY), dtype=int)


def wrap_position(x, y, LX, LY):
    return x % LX, y % LY


def is_empty(grid, x, y):
    return grid[x, y] == EMPTY


def place_agent(grid, x, y, value):
    assert is_empty(grid, x, y), "Cell already occupied"
    grid[x, y] = value


def remove_agent(grid, x, y):
    grid[x, y] = EMPTY


def move_agent(grid, old_x, old_y, new_x, new_y, value):
    if is_empty(grid, new_x, new_y):
        grid[old_x, old_y] = EMPTY
        grid[new_x, new_y] = value
        return True
    return False


def get_neighbors(x, y, LX, LY):
    return [
        wrap_position(x + 1, y, LX, LY),
        wrap_position(x - 1, y, LX, LY),
        wrap_position(x, y + 1, LX, LY),
        wrap_position(x, y - 1, LX, LY),
    ]