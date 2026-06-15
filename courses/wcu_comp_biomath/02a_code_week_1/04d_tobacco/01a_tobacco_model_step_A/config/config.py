"""
Configuration for Version A of the tobacco ecosystem model.

Version A includes:
- plant grid
- adult moth agents
- eggs and caterpillars on the grid
- predator agents (big-eyed bugs)
- plant damage and simple recovery
- day/night cycle
"""

GRID_HEIGHT = 30
GRID_WIDTH = 30

N_STEPS = 200
RANDOM_SEED = 42

# Day / night cycle
DAY_LENGTH = 10
NIGHT_LENGTH = 10

# Plants
INITIAL_PLANT_HEALTH = 1.0
PLANT_RECOVERY_RATE = 0.003
PLANT_MAX_HEALTH = 1.0
PLANT_MIN_HEALTH = 0.0

# Moths
N_MOTHS = 25
MOTH_MOVE_RADIUS = 1              # local motion
MOTH_EGG_LAYING_PROB = 0.25       # per moth per night step
MOTH_PREFERRED_HEALTH_WEIGHT = 1.0

# Eggs and caterpillars
EGG_HATCH_DELAY = 4
CATERPILLAR_DAMAGE_RATE = 0.015   # plant damage per caterpillar per step
CATERPILLAR_BACKGROUND_MORTALITY = 0.01

# Predators
N_PREDATORS = 10
PREDATOR_MOVE_RADIUS = 1
PREDATOR_CONSUMPTION_RATE = 2     # max caterpillars eaten by one predator per step
PREDATOR_BIAS_TO_PREY = 2.0       # weight for moving toward prey-rich cells

# Output and diagnostics
DEBUG = True
PRINT_EVERY = 10
SNAPSHOT_EVERY = 5
OUTPUT_DIR = "outputs"
GIF_NAME = "tobacco_version_a.gif"