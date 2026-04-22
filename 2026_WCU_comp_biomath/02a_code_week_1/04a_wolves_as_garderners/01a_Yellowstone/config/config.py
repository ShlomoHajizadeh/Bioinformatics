"""
Configuration parameters for Yellowstone simulation.
"""

# Grid dimensions
NX = 50  # Grid width
NY = 50  # Grid height

# Agent counts
N_BISON = 300
N_WOLVES = 15

# Movement parameters
WOLF_MOVE_PERIOD = 1  # Wolves move every k steps

# Simulation parameters
N_STEPS = 5#500
RANDOM_SEED = 42

# Cell types
CELL_TYPE_GRASS = "grass"
CELL_TYPE_FOREST = "forest"

# Initial environment setup
INITIAL_FOREST_FRACTION = 0.15  # 15% of cells start as forest
INITIAL_GRASS_STAGE_MEAN = 4.0  # Mean initial grass stage (0-10 scale)
INITIAL_GRASS_STAGE_STD = 1.0   # Standard deviation of initial grass stage

# Grass stage parameters (0-10 scale)
MIN_GRASS_STAGE = 0   # Overgrazed
MAX_GRASS_STAGE = 10  # Emerging forest
GRASS_PREFERENCE_THRESHOLD = 4  # Bison prefer stages >= 4

# NEW SIMPLIFIED: Grass change rules (per time step)
GRASS_CHANGE_GRAZING = -2     # ANY bison in cell (>= 1)
GRASS_CHANGE_RECOVERY = +1    # 0 bison in cell

# Forest conversion parameters
STAGE10_THRESHOLD = 20  # Number of consecutive steps at stage 10 before conversion to forest

# Wolf-bison interaction parameters
WOLF_DETECTION_RANGE = 0  # Wolves affect bison in same cell only

# NEW: Occupancy constraints
MAX_WOLVES_PER_CELL = 1  # Maximum wolves per cell
MAX_BISON_PER_CELL = 1   # Maximum bison per cell (after resolution)

# Visualization parameters
SAVE_PLOTS = True
OUTPUT_DIR = "output"
VISUALIZATION_INTERVAL = 10  # Save visualization every N steps (for animation)