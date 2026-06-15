"""
Movement rules for targets and chasers
"""

import random

from .lattice import get_neighbors, is_empty
from .distance import (
    toroidal_distance,
    find_nearest_chaser,
    find_nearest_target,
)


def decide_target_move(target, chasers, grid, LX, LY):
    """
    Decide the next position of a target.

    Rule:
    - Find the nearest chaser.
    - Consider the four von Neumann neighbors.
    - Choose among the neighbors that maximize the distance
      to that nearest chaser.
    - If the chosen site is occupied, the target stays in place.

    Returns
    -------
    (new_x, new_y)
    """
    nearest_chasers, _ = find_nearest_chaser(target, chasers, LX, LY)

    if len(nearest_chasers) == 0:
        return target.x, target.y

    chosen_chaser = random.choice(nearest_chasers)
    candidates = get_neighbors(target.x, target.y, LX, LY)

    best_sites = []
    best_distance = -1.0

    for nx, ny in candidates:
        d = toroidal_distance(nx, ny, chosen_chaser.x, chosen_chaser.y, LX, LY)

        if d > best_distance:
            best_distance = d
            best_sites = [(nx, ny)]
        elif d == best_distance:
            best_sites.append((nx, ny))

    chosen_site = random.choice(best_sites)

    if is_empty(grid, *chosen_site):
        return chosen_site

    return target.x, target.y


def decide_chaser_move(chaser, targets, grid, LX, LY):
    """
    Decide the next action of a chaser.

    Rule:
    - Find the nearest target.
    - Consider the four von Neumann neighbors.
    - Choose among the neighbors that minimize the distance
      to a nearest target.
    - If the chosen site is empty, move there.
    - If the chosen site contains a live nearest target, this is a capture move.
    - Otherwise, the chaser stays in place.

    Returns
    -------
    dict with keys:
        "type": "move", "capture", or "stay"
        "new_x": int
        "new_y": int
        "target_id": int or None
    """
    alive_targets = [t for t in targets.values() if t.alive]
    if len(alive_targets) == 0:
        return {
            "type": "stay",
            "new_x": chaser.x,
            "new_y": chaser.y,
            "target_id": None,
        }

    nearest_targets, _ = find_nearest_target(chaser, targets, LX, LY)
    if len(nearest_targets) == 0:
        return {
            "type": "stay",
            "new_x": chaser.x,
            "new_y": chaser.y,
            "target_id": None,
        }

    candidates = get_neighbors(chaser.x, chaser.y, LX, LY)

    best_sites = []
    best_distance = float("inf")

    for nx, ny in candidates:
        site_distance = min(
            toroidal_distance(nx, ny, target.x, target.y, LX, LY)
            for target in nearest_targets
        )

        if site_distance < best_distance:
            best_distance = site_distance
            best_sites = [(nx, ny)]
        elif site_distance == best_distance:
            best_sites.append((nx, ny))

    chosen_site = random.choice(best_sites)
    nx, ny = chosen_site

    if is_empty(grid, nx, ny):
        return {
            "type": "move",
            "new_x": nx,
            "new_y": ny,
            "target_id": None,
        }

    for target in nearest_targets:
        if target.alive and (nx, ny) == (target.x, target.y):
            return {
                "type": "capture",
                "new_x": nx,
                "new_y": ny,
                "target_id": target.id,
            }

    return {
        "type": "stay",
        "new_x": chaser.x,
        "new_y": chaser.y,
        "target_id": None,
    }