
import random
import numpy as np
import matplotlib.pyplot as plt

from config.config import *
from environment.lattice import Lattice
from agents.base_agent import BaseAgent


class Simulation:
    def __init__(self):
        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)

        self.lattice = Lattice(GRID_WIDTH, GRID_HEIGHT, RANDOM_SEED)
        self.agents = []
        self.time = 0

        self.history = {k: [] for k in INIT_POP.keys()}

        self.initialize_agents()

    def initialize_agents(self):
        for species, count in INIT_POP.items():
            for _ in range(count):
                x = np.random.randint(0, GRID_HEIGHT)
                y = np.random.randint(0, GRID_WIDTH)

                agent = BaseAgent(species, x, y)

                # ensure valid placement
                if self.lattice.get_habitat(x, y) in agent.allowed_habitats():
                    self.agents.append(agent)

    def step(self):
        for agent in self.agents:
            if agent.alive:
                agent.step(self.lattice)

        self.time += 1
        self.record()

    def record(self):
        counts = {k: 0 for k in INIT_POP.keys()}
        for agent in self.agents:
            if agent.alive:
                counts[agent.species] += 1

        for k in counts:
            self.history[k].append(counts[k])

    def run(self):
        for _ in range(TIME_STEPS):
            self.step()

    def plot(self):
        for species, values in self.history.items():
            plt.plot(values, label=species)

        plt.legend()
        plt.xlabel("time")
        plt.ylabel("population")
        plt.title("Invasive Species Simulation (Baseline)")
        plt.show()
