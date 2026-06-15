"""
Configuration for the Prisoner's Dilemma evolutionary tournament.

Phase 3:
High temptation to defect
Purpose:
Show how environmental incentives shape cooperation.
"""

# -----------------------------
# Game settings
# -----------------------------
ROUNDS_PER_MATCH = 10

# Payoff notation:
# R = reward for mutual cooperation
# T = temptation to defect
# P = punishment for mutual defection
# S = sucker's payoff
#
# Standard Prisoner's Dilemma ordering:
# T > R > P > S
#
# In this phase, we increase T to make defection more attractive.
PAYOFF_NAME = "high_temptation"

R = 3
T = 10
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