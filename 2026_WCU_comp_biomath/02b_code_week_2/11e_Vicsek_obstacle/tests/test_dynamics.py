"""Tests for dynamics functions (position updates, heading updates)."""
import pytest
import numpy as np
from config import VicsekConfig
from dynamics import update_positions, update_headings
from neighborhood import find_neighbors


class TestPeriodicBoundaryConditions:
    """Tests for periodic boundary wrapping in position updates."""
    
    def test_simple_wrap_right(self):
        """Test wrapping when particle moves past right boundary."""
        config = VicsekConfig(N=1, L=10.0, h=1.0, nu_0=1.0)
        
        positions = np.array([[9.5, 5.0]])  # Near right edge
        headings = np.array([0.0])  # Moving right (east)
        
        new_positions = update_positions(positions, headings, config)
        
        # Should wrap to x = 0.5
        assert new_positions[0, 0] == pytest.approx(0.5, abs=1e-10)
        assert new_positions[0, 1] == pytest.approx(5.0, abs=1e-10)
    
    def test_simple_wrap_top(self):
        """Test wrapping when particle moves past top boundary."""
        config = VicsekConfig(N=1, L=10.0, h=1.0, nu_0=2.0)
        
        positions = np.array([[5.0, 9.0]])  # Near top edge
        headings = np.array([np.pi/2])  # Moving up (north)
        
        new_positions = update_positions(positions, headings, config)
        
        # Should wrap to y = 1.0
        assert new_positions[0, 0] == pytest.approx(5.0, abs=1e-10)
        assert new_positions[0, 1] == pytest.approx(1.0, abs=1e-10)
    
    def test_simple_wrap_left(self):
        """Test wrapping when particle moves past left boundary."""
        config = VicsekConfig(N=1, L=10.0, h=1.0, nu_0=1.0)
        
        positions = np.array([[0.3, 5.0]])  # Near left edge
        headings = np.array([np.pi])  # Moving left (west)
        
        new_positions = update_positions(positions, headings, config)
        
        # Should wrap to x = 9.3
        assert new_positions[0, 0] == pytest.approx(9.3, abs=1e-10)
        assert new_positions[0, 1] == pytest.approx(5.0, abs=1e-10)
    
    def test_no_wrap_needed(self):
        """Test that positions stay in bounds when no wrapping needed."""
        config = VicsekConfig(N=1, L=10.0, h=1.0, nu_0=0.5)
        
        positions = np.array([[5.0, 5.0]])  # Center
        headings = np.array([np.pi/4])  # Moving northeast
        
        new_positions = update_positions(positions, headings, config)
        
        # Should stay in [0, 10)
        assert 0 <= new_positions[0, 0] < 10.0
        assert 0 <= new_positions[0, 1] < 10.0
    
    def test_multiple_particles(self):
        """Test position updates for multiple particles."""
        config = VicsekConfig(N=3, L=10.0, h=1.0, nu_0=1.0)
        
        positions = np.array([
            [5.0, 5.0],
            [9.5, 5.0],
            [5.0, 9.5]
        ])
        headings = np.array([0.0, 0.0, np.pi/2])  # East, East, North
        
        new_positions = update_positions(positions, headings, config)
        
        # Particle 0: no wrap
        assert new_positions[0, 0] == pytest.approx(6.0, abs=1e-10)
        assert new_positions[0, 1] == pytest.approx(5.0, abs=1e-10)
        
        # Particle 1: wraps in x
        assert new_positions[1, 0] == pytest.approx(0.5, abs=1e-10)
        assert new_positions[1, 1] == pytest.approx(5.0, abs=1e-10)
        
        # Particle 2: wraps in y
        assert new_positions[2, 0] == pytest.approx(5.0, abs=1e-10)
        assert new_positions[2, 1] == pytest.approx(0.5, abs=1e-10)


class TestPositionUpdate:
    """Tests for position update mechanics."""
    
    def test_positions_shape_preserved(self):
        """Position updates should preserve array shape."""
        config = VicsekConfig(N=10, L=10.0, h=1.0, nu_0=0.5)
        
        positions = np.random.uniform(0, 10.0, size=(10, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=10)
        
        new_positions = update_positions(positions, headings, config)
        
        assert new_positions.shape == (10, 2)
    
    def test_positions_always_in_bounds(self):
        """All updated positions should be in [0, L)."""
        config = VicsekConfig(N=50, L=10.0, h=1.0, nu_0=2.0, seed=42)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(50, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=50)
        
        new_positions = update_positions(positions, headings, config)
        
        assert np.all(new_positions >= 0), "Some positions < 0"
        assert np.all(new_positions < 10.0), "Some positions >= L"


class TestHeadingUpdate:
    """Tests for heading update mechanics."""
    
    def test_headings_shape_preserved(self):
        """Heading updates should preserve array shape."""
        config = VicsekConfig(N=10, L=10.0, r=2.0, eta=0.1, seed=42)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(10, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=10)
        
        new_headings = update_headings(headings, positions, config)
        
        assert new_headings.shape == (10,)
    
    def test_headings_in_valid_range(self):
        """Updated headings should be in [-π, π]."""
        config = VicsekConfig(N=20, L=10.0, r=2.0, eta=0.5, seed=42)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(20, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=20)
        
        new_headings = update_headings(headings, positions, config)
        
        assert np.all(new_headings >= -np.pi), "Some headings < -π"
        assert np.all(new_headings <= np.pi), "Some headings > π"
    
    def test_zero_noise_isolated_particle(self):
        """Isolated particle with zero noise should keep same heading."""
        config = VicsekConfig(N=1, L=10.0, r=1.0, eta=0.0, seed=42)
        
        np.random.seed(42)
        positions = np.array([[5.0, 5.0]])
        headings = np.array([np.pi/4])
        
        new_headings = update_headings(headings, positions, config)
        
        # With no neighbors (except self) and no noise, heading should stay same
        assert new_headings[0] == pytest.approx(np.pi/4, abs=1e-10)
    
    def test_aligned_neighbors_zero_noise(self):
        """Particles with aligned neighbors and zero noise should maintain alignment."""
        config = VicsekConfig(N=3, L=10.0, r=2.0, eta=0.0, seed=42)
        
        np.random.seed(42)
        # Three particles close together
        positions = np.array([
            [5.0, 5.0],
            [5.5, 5.0],
            [5.0, 5.5]
        ])
        # All heading in same direction
        headings = np.array([np.pi/3, np.pi/3, np.pi/3])
        
        new_headings = update_headings(headings, positions, config)
        
        # All should keep same heading (perfect alignment)
        for heading in new_headings:
            assert heading == pytest.approx(np.pi/3, abs=1e-10)
    
    def test_noise_changes_headings(self):
        """Non-zero noise should cause heading changes."""
        config = VicsekConfig(N=10, L=10.0, r=1.0, eta=1.0, seed=42)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(10, 2))
        headings = np.array([0.0] * 10)  # All same initially
        
        new_headings = update_headings(headings, positions, config)
        
        # With noise, headings should differ
        assert not np.allclose(new_headings, headings), \
            "Headings should change with non-zero noise"
    
    def test_heading_update_reproducibility(self):
        """Same seed should give reproducible heading updates."""
        config1 = VicsekConfig(N=5, L=10.0, r=2.0, eta=0.5, seed=123)
        config2 = VicsekConfig(N=5, L=10.0, r=2.0, eta=0.5, seed=123)
        
        positions = np.array([
            [2.0, 3.0],
            [2.5, 3.0],
            [3.0, 3.0],
            [7.0, 7.0],
            [8.0, 8.0]
        ])
        headings = np.array([0.1, 0.2, 0.15, 1.0, 1.1])
        
        np.random.seed(123)
        new_headings1 = update_headings(headings, positions, config1)
        
        np.random.seed(123)
        new_headings2 = update_headings(headings, positions, config2)
        
        assert np.allclose(new_headings1, new_headings2), \
            "Same seed should give same heading updates"