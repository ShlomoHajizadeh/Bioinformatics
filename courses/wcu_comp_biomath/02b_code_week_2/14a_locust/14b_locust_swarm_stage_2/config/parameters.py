"""
Configuration parameters for the locust swarm simulation.
Stage 2: Add gravity and ground boundary.
"""

# Number of locusts
N = 50

# Social interaction parameters
#F = 0.5   # Attraction strength (F < 1)
#L = 10.0  # Attraction length scale (L > 1)

# Note: F=0.5, L=10 corresponds to catastrophic regime (bubble formation)
# For H-stable regime, use F=0.25, L=1.5

F = 0.25
L = 1.5

# Forces
G = 1.0   # Gravity strength (Stage 2: enabled)
U = 0.0   # Wind speed (Stage 2: disabled, will be used in Stage 3)

# Time parameters
dt = 0.01          # Time step
T_total = 30.0     # Total simulation time

# Domain size (for initialization)
domain_size = 10.0
initial_height = 5.0  # Initial height above ground

# Random seed for reproducibility
random_seed = 42

# Plotting options
plot_interval = 50      # Plot every N steps
save_animation = True   # Save animation as GIF
animation_fps = 15      # Frames per second for animation