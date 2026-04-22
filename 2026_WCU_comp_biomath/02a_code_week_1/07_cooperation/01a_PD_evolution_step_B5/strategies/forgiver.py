"""
Strategy: Forgiver.

- Start with cooperation.
- If the opponent defects, punish by defecting for a short time.
- Then return to cooperation.

This strategy is useful in noisy environments because it does not
hold a permanent grudge.
"""

from strategies.base_strategy import BaseStrategy


class Forgiver(BaseStrategy):
    def __init__(self, punishment_length=1):
        super().__init__(name="Forgiver")
        self.punishment_length = punishment_length
        self.remaining_punishment = 0

    def reset(self):
        self.remaining_punishment = 0

    def choose_action(self, opponent_history, own_history):
        if self.remaining_punishment > 0:
            self.remaining_punishment -= 1
            return "D"

        if opponent_history and opponent_history[-1] == "D":
            self.remaining_punishment = self.punishment_length
            self.remaining_punishment -= 1
            return "D"

        return "C"