"""Tests for neighborhood detection and periodic distance calculations."""
import pytest
import numpy as np
from config import VicsekConfig
from neighborhood import periodic_distance, find_neighbors


class TestPeriodicDistance:
    """Tests for periodic distance calculation."""
    
    def test_distance_same_point(self):
        """Distance from a point to itself should be zero."""
        p1 = np.array([5.0, 5.0])
        p2 = np.array([5.0, 5.0])
        L = 10.0
        
        dist = periodic_distance(p1, p2, L)
        
        assert dist == pytest.approx(0.0, abs=1e-10)
    
    def test_distance_direct(self):
        """Test direct distance (no wrapping needed)."""
        p1 = np.array([2.0, 3.0])
        p2 = np.array([5.0, 7.0])
        L = 10.0
        
        dist = periodic_distance(p1, p2, L)
        expected = np.sqrt((5.0 - 2.0)**2 + (7.0 - 3.0)**2)  # = 5.0
        
        assert dist == pytest.approx(expected, abs=1e-10)
    
    def test_distance_wrapped_x(self):
        """Test distance with wrapping in x-direction."""
        p1 = np.array([1.0, 5.0])
        p2 = np.array([9.0, 5.0])
        L = 10.0
        
        # Direct distance would be 8.0, but wrapped is 2.0
        dist = periodic_distance(p1, p2, L)
        
        assert dist == pytest.approx(2.0, abs=1e-10)
    
    def test_distance_wrapped_y(self):
        """Test distance with wrapping in y-direction."""
        p1 = np.array([5.0, 1.0])
        p2 = np.array([5.0, 9.0])
        L = 10.0
        
        # Direct distance would be 8.0, but wrapped is 2.0
        dist = periodic_distance(p1, p2, L)
        
        assert dist == pytest.approx(2.0, abs=1e-10)
    
    def test_distance_wrapped_both(self):
        """Test distance with wrapping in both directions."""
        p1 = np.array([1.0, 1.0])
        p2 = np.array([9.0, 9.0])
        L = 10.0
        
        # Direct distance would be sqrt(8^2 + 8^2) ≈ 11.3
        # Wrapped distance is sqrt(2^2 + 2^2) ≈ 2.83
        dist = periodic_distance(p1, p2, L)
        expected = np.sqrt(2.0**2 + 2.0**2)
        
        assert dist == pytest.approx(expected, abs=1e-10)
    
    def test_distance_symmetry(self):
        """Distance should be symmetric: d(p1, p2) = d(p2, p1)."""
        p1 = np.array([2.0, 8.0])
        p2 = np.array([7.0, 1.0])
        L = 10.0
        
        dist1 = periodic_distance(p1, p2, L)
        dist2 = periodic_distance(p2, p1, L)
        
        assert dist1 == pytest.approx(dist2, abs=1e-10)


class TestNeighborDetection:
    """Tests for neighbor detection using find_neighbors."""
    
    def test_particle_is_own_neighbor(self):
        """Each particle should include itself in its neighborhood."""
        config = VicsekConfig(N=3, L=10.0, r=1.0)
        
        # Particles far apart
        positions = np.array([
            [2.0, 2.0],
            [5.0, 5.0],
            [8.0, 8.0]
        ])
        
        neighbors = find_neighbors(positions, config)
        
        # Each particle should at least have itself
        for i in range(3):
            assert i in neighbors[i], f"Particle {i} not in its own neighborhood"
    
    def test_close_particles_are_neighbors(self):
        """Particles within radius r should be neighbors."""
        config = VicsekConfig(N=3, L=10.0, r=2.0)
        
        positions = np.array([
            [5.0, 5.0],  # Particle 0
            [6.0, 5.0],  # Particle 1: distance 1.0 from particle 0
            [5.0, 6.5]   # Particle 2: distance 1.5 from particle 0
        ])
        
        neighbors = find_neighbors(positions, config)
        
        # Particle 0 should have particles 1 and 2 as neighbors
        assert 1 in neighbors[0], "Particle 1 should be neighbor of 0"
        assert 2 in neighbors[0], "Particle 2 should be neighbor of 0"
        
        # Symmetry: particle 1 should have particle 0 as neighbor
        assert 0 in neighbors[1], "Particle 0 should be neighbor of 1"
    
    def test_distant_particles_not_neighbors(self):
        """Particles beyond radius r should not be neighbors."""
        config = VicsekConfig(N=2, L=10.0, r=1.0)
        
        positions = np.array([
            [2.0, 2.0],
            [8.0, 8.0]  # Distance > r from particle 0
        ])
        
        neighbors = find_neighbors(positions, config)
        
        # Particle 0 should only have itself
        assert neighbors[0] == [0], f"Expected [0], got {neighbors[0]}"
        
        # Particle 1 should only have itself
        assert neighbors[1] == [1], f"Expected [1], got {neighbors[1]}"
    
    def test_periodic_neighbors(self):
        """Test neighbor detection across periodic boundary."""
        config = VicsekConfig(N=2, L=10.0, r=2.0)
        
        positions = np.array([
            [0.5, 5.0],  # Particle 0
            [9.5, 5.0]   # Particle 1: wraps to be distance 1.0 from particle 0
        ])
        
        neighbors = find_neighbors(positions, config)
        
        # They should be neighbors due to periodic boundary
        assert 1 in neighbors[0], "Particle 1 should be neighbor of 0 (periodic)"
        assert 0 in neighbors[1], "Particle 0 should be neighbor of 1 (periodic)"
    
    def test_exact_radius_boundary(self):
        """Test particles exactly at radius r."""
        config = VicsekConfig(N=2, L=10.0, r=3.0)
        
        positions = np.array([
            [5.0, 5.0],
            [8.0, 5.0]  # Exactly distance 3.0 from particle 0
        ])
        
        neighbors = find_neighbors(positions, config)
        
        # Should be neighbors (distance <= r)
        assert 1 in neighbors[0], "Particle at exactly radius r should be a neighbor"
    
    def test_three_particle_chain(self):
        """Test neighborhood in a simple 3-particle configuration."""
        config = VicsekConfig(N=3, L=10.0, r=1.5)
        
        positions = np.array([
            [5.0, 5.0],  # Particle 0
            [6.0, 5.0],  # Particle 1: distance 1.0 from 0
            [7.5, 5.0]   # Particle 2: distance 1.5 from 1, 2.5 from 0
        ])
        
        neighbors = find_neighbors(positions, config)
        
        # Particle 0: should have 0 and 1 (not 2, too far)
        assert set(neighbors[0]) == {0, 1}, f"Expected {{0, 1}}, got {set(neighbors[0])}"
        
        # Particle 1: should have 0, 1, and 2
        assert set(neighbors[1]) == {0, 1, 2}, f"Expected {{0, 1, 2}}, got {set(neighbors[1])}"
        
        # Particle 2: should have 1 and 2 (not 0, too far)
        assert set(neighbors[2]) == {1, 2}, f"Expected {{1, 2}}, got {set(neighbors[2])}"