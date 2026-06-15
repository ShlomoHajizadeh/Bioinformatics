"""
Configuration parameters for the locust swarm simulation.
Stage 3: Add wind for rolling/marching swarm behavior.
"""

# Number of locusts
N = 50

# Social interaction parameters
# ============================================================
# STAGE 3 OPTIMIZED PARAMETERS for rolling behavior:
# ============================================================

# OPTION 1: Catastrophic regime with rolling (recommended)
# F = 0.25
# L = 10.0
# U = 2.5

# F = 0.5
# L = 10.0
# U = 2.0

# OPTION 2: H-stable regime with rolling
# F = 0.5
# L = 2.0
# U = 3.0

F = 0.25
L = 1.5
U = 3.0

# OPTION 3: Stronger wind, weaker attraction
# F = 0.3
# L = 8.0
# U = 4.0

# ============================================================

# Forces
G = 1.0   # Gravity strength

# Time parameters
dt = 0.01          # Time step
T_total = 50.0     # Total simulation time (longer for Stage 3 to see rolling)

# Domain size (for initialization)
domain_size = 20.0      # Larger domain for rolling
initial_height = 6.0    # Initial height above ground

# Random seed for reproducibility
random_seed = 42

# Plotting options
plot_interval = 50      # Plot every N steps
save_animation = True   # Save animation as GIF
animation_fps = 20      # Frames per second for animation

# Stage 3 specific parameters
track_rolling = True    # Track rolling dynamics
rolling_threshold = 0.5 # Velocity threshold to consider a locust "rolling"