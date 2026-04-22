"""
Configuration for Version C of the tobacco ecosystem model.

Version C adds:
- volatile airborne signaling
- signal diffusion / neighborhood spreading
- signal decay
- defense priming in neighboring plants
- lower effective defense threshold for primed plants
- extra caterpillar mortality on defended plants

This parameter set is chosen to produce a clearly visible
community-defense effect compared with Version B.
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
ATTACK_THRESHOLD = 2
DEFENSE_ON_THRESHOLD = 5
DEFENSE_OFF_THRESHOLD = 1
DEFENSE_INCREASE_RATE = 0.40
DEFENSE_RELAX_RATE = 0.02
DEFENSE_MAX = 1.0
DEFENSE_CATERPILLAR_MORTALITY = 0.6

# Bloom modes
BLOOM_NIGHT = 0
BLOOM_DAY = 1

# Moths
N_MOTHS = 28
MOTH_MOVE_RADIUS = 1
MOTH_EGG_LAYING_PROB = 0.30
MOTH_PREFERRED_HEALTH_WEIGHT = 1.0
MOTH_PREFERRED_BLOOM_WEIGHT = 2.5
MOTH_DEFENSE_AVOIDANCE_WEIGHT = 7.0

# Eggs and caterpillars
EGG_HATCH_DELAY = 4
CATERPILLAR_DAMAGE_RATE = 0.018
CATERPILLAR_BACKGROUND_MORTALITY = 0.01

# Predators
N_PREDATORS = 10
PREDATOR_MOVE_RADIUS = 1
PREDATOR_CONSUMPTION_RATE = 4
PREDATOR_BIAS_TO_PREY = 2.0

# Signaling and priming
SIGNAL_PRODUCTION_RATE = 1.0
SIGNAL_DIFFUSION_RATE = 0.60
SIGNAL_DECAY_RATE = 0.02
SIGNAL_MAX = 1.0

PRIMING_STRENGTH = 1.0
PRIMING_MAX = 1.0

# Output and diagnostics
DEBUG = True
PRINT_EVERY = 10
SNAPSHOT_EVERY = 5
OUTPUT_DIR = "outputs"
GIF_NAME = "tobacco_version_c.gif"