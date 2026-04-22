#-----------------------------------------
#   Computational Biomathematics 2026
#     at Western Caspian University
#
#            Florian Rupp
# 
# Disease Dynamics Monte Carlo Simulation
#-----------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from D02_initialization import initialize_agents
from D02_interaction import simulate_step
from D02v_lattice_video import time_plot  # Use time_plot for Monte Carlo results

# Simulation parameters
N = 50                   # Size of the lattice
T = 200                   # Maximum number of time steps
NS = 100                 # Initial number of susceptible individuals
NI = 20                  # Initial number of infected individuals
num_repetitions = 10     # Number of Monte Carlo runs

# Store histories for all runs
all_susceptible_history = []
all_infected_history = []

# Run Monte Carlo simulations
for run in range(num_repetitions):
    # Set the seed value of the random number generator
    seed = 42 + run  # Different seed for each run
    np.random.seed(seed)

    # Initialize the agents
    susceptible, infected = initialize_agents(N, NS, NI)

    # Store histories for the current run
    susceptible_history = []
    infected_history = []

    for step in range(T):
        susceptible, infected = simulate_step(N, susceptible, infected, infection_probability=0.9)
        susceptible_history.append(len(susceptible))
        infected_history.append(len(infected))

    all_susceptible_history.append(susceptible_history)
    all_infected_history.append(infected_history)

# Plot results
plt.figure(figsize=(10, 6))
for i in range(num_repetitions):
    line_style = '-' if i == 0 else '--'  # Solid line for first run, dotted for others
    plt.plot(all_susceptible_history[i], label=f'Susceptible Run {i+1}', linestyle=line_style, color='green', linewidth=2 if i == 0 else 1)
    plt.plot(all_infected_history[i], label=f'Infected Run {i+1}', linestyle=line_style, color='red', linewidth=2 if i == 0 else 1)

plt.xlabel('Time Step')
plt.ylabel('Population')
plt.title('Disease Dynamics Monte Carlo Simulation')
#plt.legend()
plt.ylim(0, max(max(max(all_susceptible_history)), max(max(all_infected_history))) + 10)
plt.grid()
plt.savefig('monte_carlo_simulation.png')
plt.show()