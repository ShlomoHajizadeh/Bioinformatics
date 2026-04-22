"""
Configuration for the Prisoner's Dilemma evolutionary tournament.
"""

# -----------------------------
# Game settings
# -----------------------------
ROUNDS_PER_MATCH = 10

PAYOFFS = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}

INCLUDE_SELF_PLAY = True
RANDOM_SEED = 42

# -----------------------------
# Evolution settings
# -----------------------------
GENERATIONS = 10

# Initial population sizes of strategies
INITIAL_POPULATION = {
    "AlwaysCooperate": 20,
    "AlwaysDefect": 20,
    "TitForTat": 20,
    "RandomStrategy": 20,
    "Grudger": 20,
}

# In each generation, this many individuals are moved
# from the weakest strategy to the strongest strategy.
TRANSFER_AMOUNT = 4

# Strategies with population 0 stay in the record,
# but do not participate anymore.
MIN_POPULATION = 0