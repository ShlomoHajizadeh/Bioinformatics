"""
Game mechanics for a repeated Prisoner's Dilemma match,
including optional action noise.
"""

import random

from config.config import PAYOFFS, NOISE_ENABLED, ACTION_FLIP_PROBABILITY


def get_payoff(action_a, action_b):
    """
    Return the payoff pair for the two actions.
    """
    if (action_a, action_b) not in PAYOFFS:
        raise ValueError(f"Invalid action pair: {(action_a, action_b)}")
    return PAYOFFS[(action_a, action_b)]


def flip_action(action):
    """
    Flip an action:
    C -> D
    D -> C
    """
    if action == "C":
        return "D"
    if action == "D":
        return "C"
    raise ValueError(f"Invalid action for flipping: {action}")


def apply_noise(action, noise_enabled=True, flip_probability=0.0):
    """
    Apply execution noise to an intended action.

    Parameters
    ----------
    action : str
        Intended action ('C' or 'D').
    noise_enabled : bool
        Whether action noise is enabled.
    flip_probability : float
        Probability of flipping the action.

    Returns
    -------
    actual_action : str
        Executed action after noise.
    was_flipped : bool
        True if the action was flipped.
    """
    if action not in ("C", "D"):
        raise ValueError(f"Invalid action: {action}")

    if not noise_enabled:
        return action, False

    if random.random() < flip_probability:
        return flip_action(action), True

    return action, False


def play_match(strategy_a, strategy_b, rounds):
    """
    Play a repeated match between two strategy objects.

    Strategies observe the actual executed actions, not the intended ones.

    Returns
    -------
    result : dict
        {
            "strategy_a": str,
            "strategy_b": str,
            "score_a": int,
            "score_b": int,
            "history_a": list[str],
            "history_b": list[str],
            "intended_history_a": list[str],
            "intended_history_b": list[str],
            "noise_flips_a": int,
            "noise_flips_b": int,
        }
    """
    strategy_a.reset()
    strategy_b.reset()

    history_a = []
    history_b = []

    intended_history_a = []
    intended_history_b = []

    score_a = 0
    score_b = 0

    noise_flips_a = 0
    noise_flips_b = 0

    for _ in range(rounds):
        intended_action_a = strategy_a.choose_action(
            opponent_history=history_b,
            own_history=history_a
        )
        intended_action_b = strategy_b.choose_action(
            opponent_history=history_a,
            own_history=history_b
        )

        if intended_action_a not in ("C", "D"):
            raise ValueError(f"{strategy_a.name} returned invalid action: {intended_action_a}")
        if intended_action_b not in ("C", "D"):
            raise ValueError(f"{strategy_b.name} returned invalid action: {intended_action_b}")

        actual_action_a, flipped_a = apply_noise(
            intended_action_a,
            noise_enabled=NOISE_ENABLED,
            flip_probability=ACTION_FLIP_PROBABILITY,
        )
        actual_action_b, flipped_b = apply_noise(
            intended_action_b,
            noise_enabled=NOISE_ENABLED,
            flip_probability=ACTION_FLIP_PROBABILITY,
        )

        if flipped_a:
            noise_flips_a += 1
        if flipped_b:
            noise_flips_b += 1

        payoff_a, payoff_b = get_payoff(actual_action_a, actual_action_b)

        intended_history_a.append(intended_action_a)
        intended_history_b.append(intended_action_b)

        history_a.append(actual_action_a)
        history_b.append(actual_action_b)

        score_a += payoff_a
        score_b += payoff_b

    return {
        "strategy_a": strategy_a.name,
        "strategy_b": strategy_b.name,
        "score_a": score_a,
        "score_b": score_b,
        "history_a": history_a,
        "history_b": history_b,
        "intended_history_a": intended_history_a,
        "intended_history_b": intended_history_b,
        "noise_flips_a": noise_flips_a,
        "noise_flips_b": noise_flips_b,
    }