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
# With this probability, the intended action is flipped:
# C -> D or D -> C
NOISE_ENABLED = True
ACTION_FLIP_PROBABILITY = 0.05

# -----------------------------
# Evolution settings
# -----------------------------
GENERATIONS = 15

INITIAL_POPULATION = {
    "AlwaysCooperate": 20,
    "AlwaysDefect": 20,
    "TitForTat": 20,
    "RandomStrategy": 20,
    "Grudger": 20,
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