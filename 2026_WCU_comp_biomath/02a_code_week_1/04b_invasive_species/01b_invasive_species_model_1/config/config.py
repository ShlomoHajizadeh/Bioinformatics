# Global configuration

GRID_WIDTH = 30
GRID_HEIGHT = 30

TIME_STEPS = 100

RANDOM_SEED = 42

# Initial populations
INIT_POP = {
    "NT": 60,   # native trout
    "IT": 0,    #18,   # invasive trout
    "B": 8,     # bears
    "P": 12,    # birds
    "E": 30     # elk
}

# Movement directions: North, East, South, West, Stay
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]

# Hunting probabilities
HUNTING = {
    "IT_on_NT": 0.45,   # invasive trout on native trout in lake
    "P_on_NT": 0.60,    # birds on native trout in lake
    "B_on_NT": 0.75,    # bears on native trout in river
    "B_on_E": 0.25      # bears on elk in grassland
}

# Species-specific maximum ages
MAX_AGE = {
    "NT": 40,
    "IT": 35,
    "B": 60,
    "P": 45,
    "E": 50
}

# Per-step birth probabilities
BIRTH_RATES = {
    "NT": 0.08,
    "IT": 0.06,
    "B": 0.03,
    "P": 0.04,
    "E": 0.05
}

# Total carrying capacities
CARRYING_CAPACITY = {
    "NT": 140,
    "IT": 90,
    "E": 120
}

# Feeding constraints
BIRD_STARVE_AFTER = 12
BEAR_STARVE_NT_AFTER = 7
BEAR_STARVE_E_AFTER = 12

# Movement / sensing
SENSING_RADIUS = 3

# Visualization
PLOT_EVERY = 1