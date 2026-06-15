"""
Strategy: Grudger.
Cooperate until the opponent defects once, then defect forever.
"""

from strategies.base_strategy import BaseStrategy


class Grudger(BaseStrategy):
    def __init__(self):
        super().__init__(name="Grudger")
        self.grudge = False

    def reset(self):
        self.grudge = False

    def choose_action(self, opponent_history, own_history):
        if "D" in opponent_history:
            self.grudge = True

        if self.grudge:
            return "D"
        return "C"