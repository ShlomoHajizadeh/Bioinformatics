#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (1st Implementation)
#-----------------------------------------

import numpy as np

from P03a_initialization import initialize_agents
from P01i_interaction import simulate_step
from P03v_lattice_video import lattice_animation, time_plot
from P01v_lattice_plot import lattice_plot

# Set the seed value of the random number generator
seed = 42
np.random.seed(seed)

# Initialize the agents
N = 5     # Size of the lattice
T = 50     # Maximum number of time steps
NF = 1   # Initial number of fish
NS = 24    # Initial number of sharks

# Fish and shark parameters
fish_breeding_time = 5
shark_breeding_time = 1
shark_starving_time = 10

# Initialize the agents
fish, sharks = initialize_agents(N, NF, NS)

# Plot the initial fish and shark distribution
lattice_plot(N, fish, sharks)

# Run the simulation and store all states
print("Running simulation...")
fish_history = [len(fish)]
shark_history = [len(sharks)]
fish_states = [fish]
shark_states = [sharks]

for step in range(T):
    if step % 5 == 0:
        print(f"Step {step}/{T}")
    fish, sharks = simulate_step(N, fish, sharks, fish_breeding_time, shark_breeding_time, shark_starving_time)
    fish_history.append(len(fish))
    shark_history.append(len(sharks))
    fish_states.append(fish)
    shark_states.append(sharks)

print("Simulation complete!")

# Plot population over time
time_plot(fish_history, shark_history)

# Create animation from stored states (optional - can be slow)
create_animation = False  # Set to True if you want the animation
if create_animation:
    print("Creating animation...")
    ani = lattice_animation(N, fish_states, shark_states)
    ani.event_source.stop()
    print("Animation complete!")

# Plot the final fish and shark distribution
lattice_plot(N, fish, sharks)