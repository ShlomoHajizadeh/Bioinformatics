"""
Strategy: random choice between cooperation and defection.
"""

import random
from strategies.base_strategy import BaseStrategy


class RandomStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="RandomStrategy")

    def choose_action(self, opponent_history, own_history):
        return random.choice(["C", "D"])