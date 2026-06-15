#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

import numpy as np

from P05a_initialization import initialize_agents
from P05i_interaction import simulate_step
from P05v_lattice_video import lattice_animation, time_plot
from P05v_lattice_plot import lattice_plot

# Set the seed value of the random number generator
seed = 42
np.random.seed(seed)

# Initialize the agents
N = 10     # Size of the lattice
T = 50    # Maximum number of time steps
NF = 40   # Initial number of fish
NS = 4    # Initial number of sharks
NH = 1    # Initial number of hunter sharks

# Fish and shark parameters
fish_breeding_time = 5
shark_breeding_time = 9
shark_starving_time = 6
hunter_breeding_time = 9
hunter_starving_time = 6
breeding_energy = 2  # Minimum resource level to breed

# Initialize the agents
fish, sharks, hunters = initialize_agents(N, NF, NS, NH)

# Plot the initial fish, shark, and hunter distribution
lattice_plot(N, fish, sharks, hunters)

# Run the simulation and store all states
print("Running simulation...")
fish_history = [len(fish)]
shark_history = [len(sharks)]
hunter_history = [len(hunters)]
fish_states = [fish]
shark_states = [sharks]
hunter_states = [hunters]

for step in range(T):
    if step % 10 == 0:
        print(f"Step {step}/{T}: Fish={len(fish)}, Sharks={len(sharks)}, Hunters={len(hunters)}")
    fish, sharks, hunters = simulate_step(N, fish, sharks, hunters, fish_breeding_time, 
                                          shark_breeding_time, shark_starving_time,
                                          hunter_breeding_time, hunter_starving_time, breeding_energy)
    fish_history.append(len(fish))
    shark_history.append(len(sharks))
    hunter_history.append(len(hunters))
    fish_states.append(fish)
    shark_states.append(sharks)
    hunter_states.append(hunters)

print("Simulation complete!")

# Plot population over time
time_plot(fish_history, shark_history, hunter_history)

# Create animation from stored states (optional - can be slow)
create_animation = False  # Set to True if you want the animation
if create_animation:
    print("Creating animation...")
    ani = lattice_animation(N, fish_states, shark_states, hunter_states)
    ani.event_source.stop()
    print("Animation complete!")

# Plot the final fish, shark, and hunter distribution
# lattice_plot(N, fish, sharks, hunters)