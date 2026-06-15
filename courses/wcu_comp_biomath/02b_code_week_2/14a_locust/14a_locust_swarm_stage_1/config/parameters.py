"""
Configuration parameters for the locust swarm simulation.
Stage 1: Free-space social swarm (no gravity, no wind).
"""

# Number of locusts
N = 50

# Social interaction parameters
F = 0.25  # Attraction strength (F < 1)
L = 1.5   # Attraction length scale (L > 1)

# Forces (Stage 1: only social interactions)
G = 0.0   # Gravity (disabled for Stage 1)
U = 0.0   # Wind speed (disabled for Stage 1)

# Time parameters
dt = 0.01          # Time step
T_total = 20.0     # Total simulation time

# Domain size (for initialization)
domain_size = 10.0

# Random seed for reproducibility
random_seed = 42

# Plotting options
plot_interval = 50      # Plot every N steps
save_animation = True   # Save animation as GIF
animation_fps = 10      # Frames per second for animation