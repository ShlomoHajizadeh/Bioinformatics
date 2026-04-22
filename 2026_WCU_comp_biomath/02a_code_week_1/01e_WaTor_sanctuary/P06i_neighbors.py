from P06i_helpers import is_in_sanctuary

def find_movement_neighbors(grid, x, y, N):
    """
    Find the unoccupied neighboring cells for movement (4 directions).
    """
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if grid[new_y][new_x] == 0:
            neighbors.append((new_x, new_y))
    return neighbors

def find_breeding_neighbors(grid, x, y, N, exclude_sanctuary=False):
    """
    Find the unoccupied neighboring cells for breeding (8 directions).
    If exclude_sanctuary is True, exclude cells in the sanctuary.
    """
    neighbors = []
    for dx, dy in [(0, 1), (-1, 1), (1, 1), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if grid[new_y][new_x] == 0:
            if exclude_sanctuary and is_in_sanctuary(new_x, new_y, N):
                continue
            neighbors.append((new_x, new_y))
    return neighbors

def find_fish_neighbors(fish_grid, x, y, N, exclude_sanctuary=True):
    """
    Find neighboring cells (4 directions) that contain fish.
    If exclude_sanctuary is True, exclude fish in sanctuary (HARD SANCTUARY).
    """
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if fish_grid[new_y][new_x] == 1:
            if exclude_sanctuary and is_in_sanctuary(new_x, new_y, N):
                continue
            neighbors.append((new_x, new_y))
    return neighbors

def find_fish_neighbors_8(fish_grid, x, y, N, exclude_sanctuary=True):
    """
    Find neighboring cells (8 directions) that contain fish.
    Returns the first fish found in the order checked.
    If exclude_sanctuary is True, exclude fish in sanctuary (HARD SANCTUARY).
    """
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        new_x = (x + dx) % N
        new_y = (y + dy) % N
        if fish_grid[new_y][new_x] == 1:
            if exclude_sanctuary and is_in_sanctuary(new_x, new_y, N):
                continue
            return (new_x, new_y)
    return None