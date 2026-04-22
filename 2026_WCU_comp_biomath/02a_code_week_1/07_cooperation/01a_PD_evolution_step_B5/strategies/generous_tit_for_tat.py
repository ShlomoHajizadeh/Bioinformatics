"""
Strategy: Generous Tit for Tat.

- Start with cooperation.
- If the opponent cooperated last round, cooperate.
- If the opponent defected last round, usually defect,
  but sometimes forgive and cooperate anyway.

This is useful in noisy environments because it can
recover from accidental defections.
"""

import random
from strategies.base_strategy import BaseStrategy


class GenerousTitForTat(BaseStrategy):
    def __init__(self, forgiveness_probability=0.3):
        super().__init__(name="GenerousTitForTat")
        self.forgiveness_probability = forgiveness_probability

    def choose_action(self, opponent_history, own_history):
        if not opponent_history:
            return "C"

        if opponent_history[-1] == "C":
            return "C"

        # Opponent defected last round: sometimes forgive
        if random.random() < self.forgiveness_probability:
            return "C"
        return "D"