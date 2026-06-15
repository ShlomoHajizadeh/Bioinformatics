"""
Capture logic
"""


def apply_capture(chaser, target, grid, old_x, old_y, new_x, new_y, CHASER):
    """
    Apply a capture event:
    - remove chaser from old site
    - place chaser on target site
    - mark target as dead

    Parameters
    ----------
    chaser : Chaser
    target : Target
    grid : numpy.ndarray
    old_x, old_y : int
        Previous chaser position
    new_x, new_y : int
        Target / new chaser position
    CHASER : int
        Integer code for chaser on lattice
    """
    grid[old_x, old_y] = 0
    grid[new_x, new_y] = CHASER

    chaser.x = new_x
    chaser.y = new_y

    target.alive = False