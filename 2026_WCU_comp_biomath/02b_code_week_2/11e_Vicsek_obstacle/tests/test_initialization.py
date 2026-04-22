"""Tests for state initialization functions."""
import pytest
import numpy as np
from config import VicsekConfig
from state import initialize_state


def test_positions_shape():
    """Test that initialized positions have correct shape."""
    config = VicsekConfig(N=10, L=5.0, seed=42)
    positions, _ = initialize_state(config)
    
    assert positions.shape == (10, 2), f"Expected shape (10, 2), got {positions.shape}"


def test_headings_shape():
    """Test that initialized headings have correct shape."""
    config = VicsekConfig(N=10, L=5.0, seed=42)
    _, headings = initialize_state(config)
    
    assert headings.shape == (10,), f"Expected shape (10,), got {headings.shape}"


def test_positions_in_bounds():
    """Test that all positions are in [0, L)."""
    config = VicsekConfig(N=50, L=10.0, seed=42)
    positions, _ = initialize_state(config)
    
    assert np.all(positions >= 0), "Some positions are negative"
    assert np.all(positions < 10.0), "Some positions are >= L"


def test_headings_in_range():
    """Test that headings are in [-π, π]."""
    config = VicsekConfig(N=50, L=10.0, seed=42)
    _, headings = initialize_state(config)
    
    assert np.all(headings >= -np.pi), "Some headings are < -π"
    assert np.all(headings <= np.pi), "Some headings are > π"


def test_initialize_state_returns_both():
    """Test that initialize_state returns positions and headings."""
    config = VicsekConfig(N=5, L=5.0, seed=42)
    result = initialize_state(config)
    
    assert isinstance(result, tuple), "initialize_state should return a tuple"
    assert len(result) == 2, "initialize_state should return exactly 2 values"


def test_reproducibility_with_seed():
    """Test that same seed produces same initialization."""
    config1 = VicsekConfig(N=10, L=5.0, seed=123)
    config2 = VicsekConfig(N=10, L=5.0, seed=123)
    
    positions1, headings1 = initialize_state(config1)
    positions2, headings2 = initialize_state(config2)
    
    assert np.allclose(positions1, positions2), "Positions differ with same seed"
    assert np.allclose(headings1, headings2), "Headings differ with same seed"


def test_different_seeds_produce_different_states():
    """Test that different seeds produce different initializations."""
    config1 = VicsekConfig(N=100, L=10.0, seed=42)
    config2 = VicsekConfig(N=100, L=10.0, seed=99)
    
    positions1, headings1 = initialize_state(config1)
    positions2, headings2 = initialize_state(config2)
    
    # Very unlikely to be identical with different seeds
    assert not np.allclose(positions1, positions2), "Positions identical with different seeds"
    assert not np.allclose(headings1, headings2), "Headings identical with different seeds"