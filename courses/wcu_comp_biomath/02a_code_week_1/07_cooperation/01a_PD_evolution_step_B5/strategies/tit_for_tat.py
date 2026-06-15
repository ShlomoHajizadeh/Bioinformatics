"""
Strategy: Tit for Tat.
Start with cooperation, then copy the opponent's previous move.
"""

from strategies.base_strategy import BaseStrategy


class TitForTat(BaseStrategy):
    def __init__(self):
        super().__init__(name="TitForTat")

    def choose_action(self, opponent_history, own_history):
        if not opponent_history:
            return "C"
        return opponent_history[-1]