"""
Configuration for the Prisoner's Dilemma evolutionary tournament.

Phase 4:
Noisy interactions
Purpose:
Show fragility and robustness of cooperation.
"""

# -----------------------------
# Game settings
# -----------------------------
ROUNDS_PER_MATCH = 10

PAYOFF_NAME = "high_temptation_with_noise"

R = 3
T = 7
P = 1
S = 0

PAYOFFS = {
    ("C", "C"): (R, R),
    ("C", "D"): (S, T),
    ("D", "C"): (T, S),
    ("D", "D"): (P, P),
}

INCLUDE_SELF_PLAY = True
RANDOM_SEED = 42

# -----------------------------
# Noise settings
# -----------------------------
NOISE_ENABLED = True
ACTION_FLIP_PROBABILITY = 0.05

# -----------------------------
# Evolution settings
# -----------------------------
GENERATIONS = 15

INITIAL_POPULATION = {
    "AlwaysCooperate": 15,
    "AlwaysDefect": 15,
    "TitForTat": 15,
    "RandomStrategy": 15,
    "Grudger": 15,
    "GenerousTitForTat": 15,
    "TitForTwoTats": 15,
    "Forgiver": 15,
}

# Choose update rule:
# "replicator" or "threshold_extinction"
EVOLUTION_MODE = "replicator"

# -----------------------------
# Parameters for replicator-like update
# -----------------------------
REPLICATOR_RATE = 0.20

# -----------------------------
# Parameters for threshold extinction
# -----------------------------
EXTINCTION_THRESHOLD = 2.0
REDISTRIBUTE_EXTINCT_POPULATION = True

# -----------------------------
# Strategy-specific parameters
# -----------------------------
GENEROUS_TIT_FOR_TAT_FORGIVENESS_PROBABILITY = 0.30
FORGIVER_PUNISHMENT_LENGTH = 1