#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Wa-Tor Simulation (2nd Implementation)
#-----------------------------------------

import numpy as np
from P06a_initialization import initialize_agents
from P06i_interaction import simulate_step
from P06v_lattice_plot import lattice_plot
from P06v_lattice_video import lattice_animation, time_plot

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
N = 50  # Grid size
fish_count = 500
shark_count = 50
hunter_count = 10

# Breeding and starving times
fish_breeding_time = 3
shark_breeding_time = 10
shark_starving_time = 5
hunter_breeding_time = 15
hunter_starving_time = 8
breeding_energy = 10

# Simulation parameters
num_steps = 200

# Initialize agents
fish, sharks, hunters = initialize_agents(N, fish_count, shark_count, hunter_count)

# Storage for animation
fish_history = [fish]
shark_history = [sharks]
hunter_history = [hunters]

# Storage for population counts
fish_count_history = [len(fish)]
shark_count_history = [len(sharks)]
hunter_count_history = [len(hunters)]

# Run simulation
print("Running simulation...")
for step in range(num_steps):
    fish, sharks, hunters = simulate_step(N, fish, sharks, hunters, 
                                         fish_breeding_time, shark_breeding_time, shark_starving_time,
                                         hunter_breeding_time, hunter_starving_time, breeding_energy)
    
    fish_history.append(fish)
    shark_history.append(sharks)
    hunter_history.append(hunters)
    
    fish_count_history.append(len(fish))
    shark_count_history.append(len(sharks))
    hunter_count_history.append(len(hunters))
    
    if step % 10 == 0:
        print(f"Step {step}: Fish={len(fish)}, Sharks={len(sharks)}, Hunters={len(hunters)}")

print("Simulation complete!")

# Create final state plot
print("\nCreating final state plot...")
lattice_plot(N, fish, sharks, hunters)

# Create population time series plot
print("Creating population time series plot...")
time_plot(fish_count_history, shark_count_history, hunter_count_history)

# Create animation
print("Creating animation...")
ani = lattice_animation(N, fish_history, shark_history, hunter_history, save_gif=True)

print("\nAll visualizations complete!")
print(f"Final populations: Fish={len(fish)}, Sharks={len(sharks)}, Hunters={len(hunters)}")