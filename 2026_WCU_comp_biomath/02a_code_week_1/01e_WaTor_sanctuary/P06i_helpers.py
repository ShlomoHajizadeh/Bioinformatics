#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

def is_in_sanctuary(x, y, N):
    """
    Check if a position is within the sanctuary area.
    Sanctuary is the square from (N//4, N//4) to (3*N//4, 3*N//4)
    """
    sanctuary_start = N // 4
    sanctuary_end = 3 * N // 4
    return sanctuary_start <= x < sanctuary_end and sanctuary_start <= y < sanctuary_end

def get_direction_move(x, y, direction, N, check_sanctuary=False):
    """
    Get the new position based on current position and direction.
    Direction: 1=North, 2=East, 3=South, 4=West
    
    If check_sanctuary=True and the target position is in sanctuary,
    return the original position (predator stays in place).
    """
    if direction == 1:  # North
        new_x, new_y = x, (y + 1) % N
    elif direction == 2:  # East
        new_x, new_y = (x + 1) % N, y
    elif direction == 3:  # South
        new_x, new_y = x, (y - 1) % N
    else:  # direction == 4, West
        new_x, new_y = (x - 1) % N, y
    
    # If checking sanctuary and target is inside, stay in place
    if check_sanctuary and is_in_sanctuary(new_x, new_y, N):
        return x, y
    
    return new_x, new_y