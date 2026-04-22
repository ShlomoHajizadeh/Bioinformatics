import numpy as np
import pytest

from core.agents import Target, Chaser
from core.utils import validate_positions, validate_unique_positions


def test_validate_positions_accepts_valid_agents():
    targets = {0: Target(id=0, x=1, y=1)}
    validate_positions(targets, 10, 10)


def test_validate_positions_rejects_invalid_agents():
    targets = {0: Target(id=0, x=10, y=1)}
    with pytest.raises(AssertionError):
        validate_positions(targets, 10, 10)


def test_validate_unique_positions_rejects_overlap():
    targets = {0: Target(id=0, x=2, y=2)}
    chasers = {0: Chaser(id=0, x=2, y=2)}

    with pytest.raises(AssertionError):
        validate_unique_positions(targets, chasers)