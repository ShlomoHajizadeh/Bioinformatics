"""
Strategy: always defect.
"""

from strategies.base_strategy import BaseStrategy


class AlwaysDefect(BaseStrategy):
    def __init__(self):
        super().__init__(name="AlwaysDefect")

    def choose_action(self, opponent_history, own_history):
        return "D"