"""
Configuration for Version B of the tobacco ecosystem model.

Version B adds:
- attacked state
- inducible defense
- defense relaxation
- bloom mode switching:
    normal plants bloom at night
    defended plants bloom at day
- reduced moth attraction and egg laying on defended plants
"""

GRID_HEIGHT = 30
GRID_WIDTH = 30

N_STEPS = 250
RANDOM_SEED = 42

# Day / night cycle
DAY_LENGTH = 10
NIGHT_LENGTH = 10

# Plants
INITIAL_PLANT_HEALTH = 1.0
PLANT_RECOVERY_RATE = 0.003
PLANT_MAX_HEALTH = 1.0
PLANT_MIN_HEALTH = 0.0

# Defense
ATTACK_THRESHOLD = 2                 # caterpillars needed to mark plant as attacked
DEFENSE_ON_THRESHOLD = 3             # caterpillars needed to activate defense
DEFENSE_OFF_THRESHOLD = 1            # if below this, defense can relax
DEFENSE_INCREASE_RATE = 0.20
DEFENSE_RELAX_RATE = 0.05
DEFENSE_MAX = 1.0

# Bloom modes
BLOOM_NIGHT = 0
BLOOM_DAY = 1

# Moths
N_MOTHS = 25
MOTH_MOVE_RADIUS = 1
MOTH_EGG_LAYING_PROB = 0.25
MOTH_PREFERRED_HEALTH_WEIGHT = 1.0
MOTH_PREFERRED_BLOOM_WEIGHT = 2.0
MOTH_DEFENSE_AVOIDANCE_WEIGHT = 2.5

# Eggs and caterpillars
EGG_HATCH_DELAY = 4
CATERPILLAR_DAMAGE_RATE = 0.015
CATERPILLAR_BACKGROUND_MORTALITY = 0.01

# Predators
N_PREDATORS = 10
PREDATOR_MOVE_RADIUS = 1
PREDATOR_CONSUMPTION_RATE = 2
PREDATOR_BIAS_TO_PREY = 2.0

# Output and diagnostics
DEBUG = True
PRINT_EVERY = 10
SNAPSHOT_EVERY = 5
OUTPUT_DIR = "outputs"
GIF_NAME = "tobacco_version_b.gif"