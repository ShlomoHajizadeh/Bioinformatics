#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Disease Dynamics Simulation
#-----------------------------------------

import numpy as np
from D01_initialization  import initialize_agents
from D01_interaction     import simulate_step
from D01v_lattice_video  import lattice_animation, time_plot
from D01v_lattice_plot   import lattice_plot

# Set the seed value of the random number generator
seed = 42
np.random.seed(seed)

# Initialize the agents
N  = 50       # Size of the lattice
T  = 100       # Maximum number of time steps
NS = 100      # Initial number of susceptible individuals
NI = 20       # Initial number of infected individuals
infection_probability = 0.9  # Probability of infection

# Initialize the agents
susceptible, infected = initialize_agents(N, NS, NI)

# Run the simulation
susceptible_history = []
infected_history = []

for step in range(T):
    susceptible, infected = simulate_step(N, susceptible, infected, infection_probability)
    susceptible_history.append(len(susceptible))
    infected_history.append(len(infected))

# Pass infection_probability to the animation
ani = lattice_animation(N, susceptible, infected, T, infection_probability)
ani.event_source.stop()
time_plot(susceptible_history, infected_history)

# Plot the final distribution of susceptible and infected individuals
lattice_plot(N, susceptible, infected)