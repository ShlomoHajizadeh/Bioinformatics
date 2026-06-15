#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (1st Implementation)
#-----------------------------------------

import numpy as np

from P01a_initialization import initialize_agents
from P01m_movement       import simulate_step
from P01v_lattice_video  import lattice_animation, time_plot
from P01v_lattice_plot   import lattice_plot

# Set the seed value of the random number generator
seed = 42
np.random.seed(seed)

# Initialize the agents
N  = 50     # Size of the lattice
T  = 20     # Maximum number of time steps
NF = 100    # Initial number of fish
NS = 20     # Initial number of sharks

# Initialize the agents
fish, sharks = initialize_agents(N, NF, NS)

# Plot the initial fish and shark distribution
# lattice_plot(N, fish, sharks)

# Run the simulation
fish_history = []
shark_history = []

for step in range(T):
    fish, sharks = simulate_step(N, fish, sharks)
    fish_history.append(len(fish))
    shark_history.append(len(sharks))

ani = lattice_animation(N, fish, sharks, T)
ani.event_source.stop()
time_plot(fish_history, shark_history)

# Plot the final fish and shark distribution
lattice_plot(N, fish, sharks)