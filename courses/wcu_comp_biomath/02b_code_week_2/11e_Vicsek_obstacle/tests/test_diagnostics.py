"""Tests for diagnostic functions (order parameter, statistics, velocities)."""
import pytest
import numpy as np
from config import VicsekConfig
from diagnostics import (
    order_parameter,
    compute_velocities,
    center_of_mass,
    summary_statistics
)


class TestOrderParameter:
    """Tests for order parameter calculation."""
    
    def test_order_all_same_direction(self):
        """Order parameter should be ≈1 when all headings are equal."""
        headings = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
        order = order_parameter(headings)
        
        assert order == pytest.approx(1.0, abs=1e-10)
    
    def test_order_nearly_same_direction(self):
        """Order parameter should be close to 1 for nearly aligned headings."""
        headings = np.array([0.0, 0.01, -0.01, 0.02, -0.02])
        order = order_parameter(headings)
        
        assert order > 0.99, f"Expected order > 0.99, got {order}"
    
    def test_order_opposite_directions(self):
        """Order parameter should be ≈0 for opposite directions."""
        headings = np.array([0.0, np.pi, 0.0, np.pi])
        order = order_parameter(headings)
        
        assert order == pytest.approx(0.0, abs=1e-10)
    
    def test_order_four_cardinal_directions(self):
        """Order parameter should be ≈0 for four cardinal directions."""
        # North, East, South, West
        headings = np.array([np.pi/2, 0.0, -np.pi/2, np.pi])
        order = order_parameter(headings)
        
        assert order < 0.01, f"Expected order ≈ 0, got {order}"
    
    def test_order_perpendicular_pair(self):
        """Order parameter for two perpendicular directions."""
        # East and North
        headings = np.array([0.0, np.pi/2])
        order = order_parameter(headings)
        
        # Should be 1/√2 ≈ 0.707
        expected = 1.0 / np.sqrt(2)
        assert order == pytest.approx(expected, abs=1e-10)
    
    def test_order_random_headings_statistical(self):
        """Order parameter should be small for random headings (statistical test)."""
        np.random.seed(42)
        
        # Test multiple times with random headings
        order_values = []
        for _ in range(100):
            headings = np.random.uniform(-np.pi, np.pi, size=100)
            order = order_parameter(headings)
            order_values.append(order)
        
        mean_order = np.mean(order_values)
        
        # For large N and uniform random headings, order should be close to 0
        assert mean_order < 0.15, \
            f"Mean order for random headings should be small, got {mean_order:.3f}"
    
    def test_order_single_particle(self):
        """Order parameter for single particle should be 1."""
        headings = np.array([1.23])
        order = order_parameter(headings)
        
        assert order == pytest.approx(1.0, abs=1e-10)
    
    def test_order_range(self):
        """Order parameter should always be in [0, 1]."""
        np.random.seed(123)
        
        for _ in range(50):
            N = np.random.randint(2, 100)
            headings = np.random.uniform(-np.pi, np.pi, size=N)
            order = order_parameter(headings)
            
            assert 0.0 <= order <= 1.0, \
                f"Order parameter {order} outside [0, 1] range"
    
    def test_order_three_at_120_degrees(self):
        """Three particles at 120° apart should give order ≈ 0."""
        # Symmetrically distributed around circle
        headings = np.array([0.0, 2*np.pi/3, 4*np.pi/3])
        order = order_parameter(headings)
        
        assert order < 0.01, \
            f"Expected order ≈ 0 for symmetric distribution, got {order}"


class TestComputeVelocities:
    """Tests for velocity computation from headings."""
    
    def test_velocity_shape(self):
        """Velocities should have shape (N, 2)."""
        headings = np.array([0.0, np.pi/2, np.pi])
        nu_0 = 1.0
        
        velocities = compute_velocities(headings, nu_0)
        
        assert velocities.shape == (3, 2)
    
    def test_velocity_magnitude(self):
        """All velocities should have magnitude nu_0."""
        headings = np.array([0.0, np.pi/4, np.pi/2, np.pi, -np.pi/2])
        nu_0 = 2.5
        
        velocities = compute_velocities(headings, nu_0)
        magnitudes = np.linalg.norm(velocities, axis=1)
        
        for mag in magnitudes:
            assert mag == pytest.approx(nu_0, abs=1e-10)
    
    def test_velocity_direction_east(self):
        """Heading 0 should give velocity pointing east."""
        headings = np.array([0.0])
        nu_0 = 1.0
        
        velocities = compute_velocities(headings, nu_0)
        
        assert velocities[0, 0] == pytest.approx(1.0, abs=1e-10)  # vx
        assert velocities[0, 1] == pytest.approx(0.0, abs=1e-10)  # vy
    
    def test_velocity_direction_north(self):
        """Heading π/2 should give velocity pointing north."""
        headings = np.array([np.pi/2])
        nu_0 = 1.0
        
        velocities = compute_velocities(headings, nu_0)
        
        assert velocities[0, 0] == pytest.approx(0.0, abs=1e-10)  # vx
        assert velocities[0, 1] == pytest.approx(1.0, abs=1e-10)  # vy
    
    def test_velocity_direction_west(self):
        """Heading π should give velocity pointing west."""
        headings = np.array([np.pi])
        nu_0 = 1.0
        
        velocities = compute_velocities(headings, nu_0)
        
        assert velocities[0, 0] == pytest.approx(-1.0, abs=1e-10)  # vx
        assert velocities[0, 1] == pytest.approx(0.0, abs=1e-10)  # vy
    
    def test_velocity_scaling(self):
        """Velocities should scale linearly with nu_0."""
        headings = np.array([np.pi/4])
        
        vel1 = compute_velocities(headings, nu_0=1.0)
        vel2 = compute_velocities(headings, nu_0=2.0)
        
        assert vel2[0, 0] == pytest.approx(2 * vel1[0, 0], abs=1e-10)
        assert vel2[0, 1] == pytest.approx(2 * vel1[0, 1], abs=1e-10)


class TestCenterOfMass:
    """Tests for center of mass calculation with periodic boundaries."""
    
    def test_com_shape(self):
        """Center of mass should have shape (2,)."""
        positions = np.array([[1.0, 2.0], [3.0, 4.0]])
        L = 10.0
        
        com = center_of_mass(positions, L)
        
        assert com.shape == (2,)
    
    def test_com_simple_case(self):
        """COM of particles in center should be near center."""
        positions = np.array([
            [4.9, 5.0],
            [5.0, 4.9],
            [5.1, 5.0],
            [5.0, 5.1]
        ])
        L = 10.0
        
        com = center_of_mass(positions, L)
        
        # Should be close to (5, 5)
        assert com[0] == pytest.approx(5.0, abs=0.1)
        assert com[1] == pytest.approx(5.0, abs=0.1)
    
    def test_com_in_bounds(self):
        """Center of mass should always be in [0, L)."""
        np.random.seed(42)
        L = 10.0
        
        for _ in range(20):
            N = np.random.randint(5, 50)
            positions = np.random.uniform(0, L, size=(N, 2))
            
            com = center_of_mass(positions, L)
            
            assert 0 <= com[0] < L, f"COM x-coordinate {com[0]} not in [0, {L})"
            assert 0 <= com[1] < L, f"COM y-coordinate {com[1]} not in [0, {L})"
    
    def test_com_periodic_boundary(self):
        """COM should handle periodic boundaries correctly."""
        # Particles clustered near x=0 boundary
        positions = np.array([
            [0.5, 5.0],
            [9.5, 5.0],  # This is close to 0.5 with periodic BC
            [0.3, 5.0],
            [9.7, 5.0]
        ])
        L = 10.0
        
        com = center_of_mass(positions, L)
        
        # COM should be near 0 (or 10), not near 5
        assert com[0] < 1.0 or com[0] > 9.0, \
            f"COM should handle periodic boundary, got {com[0]}"
    
    def test_com_single_particle(self):
        """COM of single particle should be that particle's position."""
        positions = np.array([[3.7, 6.2]])
        L = 10.0
        
        com = center_of_mass(positions, L)
        
        assert com[0] == pytest.approx(3.7, abs=1e-10)
        assert com[1] == pytest.approx(6.2, abs=1e-10)


class TestSummaryStatistics:
    """Tests for summary statistics function."""
    
    def test_summary_contains_all_keys(self):
        """Summary statistics should contain all expected keys."""
        config = VicsekConfig(N=10, L=10.0, r=2.0)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(10, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=10)
        
        stats = summary_statistics(positions, headings, config)
        
        expected_keys = {
            'order_parameter',
            'center_of_mass',
            'mean_heading',
            'heading_std'
        }
        
        assert set(stats.keys()) == expected_keys, \
            f"Missing keys: {expected_keys - set(stats.keys())}"
    
    def test_summary_order_matches_direct_calculation(self):
        """Order parameter in summary should match direct calculation."""
        config = VicsekConfig(N=5, L=10.0, r=2.0)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(5, 2))
        headings = np.array([0.1, 0.2, 0.15, 0.18, 0.12])
        
        stats = summary_statistics(positions, headings, config)
        direct_order = order_parameter(headings)
        
        assert stats['order_parameter'] == pytest.approx(direct_order, abs=1e-10)
    
    def test_summary_com_matches_direct_calculation(self):
        """Center of mass in summary should match direct calculation."""
        config = VicsekConfig(N=5, L=10.0, r=2.0)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(5, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=5)
        
        stats = summary_statistics(positions, headings, config)
        direct_com = center_of_mass(positions, config.L)
        
        assert np.allclose(stats['center_of_mass'], direct_com)
    
    def test_summary_mean_heading_range(self):
        """Mean heading should be in [-π, π]."""
        config = VicsekConfig(N=10, L=10.0, r=2.0)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(10, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=10)
        
        stats = summary_statistics(positions, headings, config)
        
        assert -np.pi <= stats['mean_heading'] <= np.pi
    
    def test_summary_heading_std_positive(self):
        """Heading standard deviation should be non-negative."""
        config = VicsekConfig(N=10, L=10.0, r=2.0)
        
        np.random.seed(42)
        positions = np.random.uniform(0, 10.0, size=(10, 2))
        headings = np.random.uniform(-np.pi, np.pi, size=10)
        
        stats = summary_statistics(positions, headings, config)
        
        assert stats['heading_std'] >= 0
    
    def test_summary_identical_headings_zero_std(self):
        """Standard deviation should be zero for identical headings."""
        config = VicsekConfig(N=5, L=10.0, r=2.0)
        
        positions = np.random.uniform(0, 10.0, size=(5, 2))
        headings = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
        
        stats = summary_statistics(positions, headings, config)
        
        assert stats['heading_std'] == pytest.approx(0.0, abs=1e-10)