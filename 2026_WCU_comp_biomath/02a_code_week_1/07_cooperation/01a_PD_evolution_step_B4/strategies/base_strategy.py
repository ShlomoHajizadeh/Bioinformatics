"""
Base class for all strategies.
"""


class BaseStrategy:
    """
    Base interface for Prisoner's Dilemma strategies.
    """

    def __init__(self, name):
        self.name = name

    def reset(self):
        """
        Reset internal state before a new match.
        Override if the strategy has memory/state.
        """
        pass

    def choose_action(self, opponent_history, own_history):
        """
        Decide whether to cooperate ('C') or defect ('D').
        """
        raise NotImplementedError("Subclasses must implement choose_action().")