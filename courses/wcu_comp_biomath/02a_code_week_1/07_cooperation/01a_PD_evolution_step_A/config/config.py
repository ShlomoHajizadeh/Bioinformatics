"""
Configuration for the baseline Prisoner's Dilemma tournament.
"""

# Number of rounds per match
ROUNDS_PER_MATCH = 10

# Payoff matrix:
# (my_action, opponent_action) -> (my_payoff, opponent_payoff)
PAYOFFS = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}

# If True, each strategy also plays against itself
INCLUDE_SELF_PLAY = True

# Random seed for reproducibility
RANDOM_SEED = 42

