"""
Strategy: Tit for Two Tats.

- Start with cooperation.
- Cooperate unless the opponent defected in the last two rounds.
- Only then defect.

This makes the strategy more tolerant of isolated accidental defections.
"""

from strategies.base_strategy import BaseStrategy


class TitForTwoTats(BaseStrategy):
    def __init__(self):
        super().__init__(name="TitForTwoTats")

    def choose_action(self, opponent_history, own_history):
        if len(opponent_history) < 2:
            return "C"

        if opponent_history[-1] == "D" and opponent_history[-2] == "D":
            return "D"

        return "C"