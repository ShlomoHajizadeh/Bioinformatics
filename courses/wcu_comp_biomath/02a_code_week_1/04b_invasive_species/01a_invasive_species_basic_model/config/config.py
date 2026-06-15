# Global configuration

GRID_WIDTH = 30
GRID_HEIGHT = 30

TIME_STEPS = 100

RANDOM_SEED = 42

# Initial populations
INIT_POP = {
    "NT": 40,   # native trout
    "IT": 20,   # invasive trout
    "B": 5,     # bears
    "P": 8,     # birds
    "E": 25     # elk
}

# Movement directions (N, E, S, W)
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Visualization
PLOT_EVERY = 1
