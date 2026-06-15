"""
Strategy: always cooperate.
"""

from strategies.base_strategy import BaseStrategy


class AlwaysCooperate(BaseStrategy):
    def __init__(self):
        super().__init__(name="AlwaysCooperate")

    def choose_action(self, opponent_history, own_history):
        return "C"

