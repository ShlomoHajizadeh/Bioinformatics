"""
Game mechanics for a repeated Prisoner's Dilemma match.
"""

from config.config import PAYOFFS


def get_payoff(action_a, action_b):
    """
    Return the payoff pair for the two actions.
    """
    if (action_a, action_b) not in PAYOFFS:
        raise ValueError(f"Invalid action pair: {(action_a, action_b)}")
    return PAYOFFS[(action_a, action_b)]


def play_match(strategy_a, strategy_b, rounds):
    """
    Play a repeated match between two strategy objects.

    Returns
    -------
    result : dict
        {
            "strategy_a": str,
            "strategy_b": str,
            "score_a": int,
            "score_b": int,
            "history_a": list[str],
            "history_b": list[str]
        }
    """
    strategy_a.reset()
    strategy_b.reset()

    history_a = []
    history_b = []
    score_a = 0
    score_b = 0

    for _ in range(rounds):
        action_a = strategy_a.choose_action(opponent_history=history_b, own_history=history_a)
        action_b = strategy_b.choose_action(opponent_history=history_a, own_history=history_b)

        if action_a not in ("C", "D"):
            raise ValueError(f"{strategy_a.name} returned invalid action: {action_a}")
        if action_b not in ("C", "D"):
            raise ValueError(f"{strategy_b.name} returned invalid action: {action_b}")

        payoff_a, payoff_b = get_payoff(action_a, action_b)

        history_a.append(action_a)
        history_b.append(action_b)

        score_a += payoff_a
        score_b += payoff_b

    return {
        "strategy_a": strategy_a.name,
        "strategy_b": strategy_b.name,
        "score_a": score_a,
        "score_b": score_b,
        "history_a": history_a,
        "history_b": history_b,
    }
