import os
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from config.config import (
    GRID_WIDTH,
    GRID_HEIGHT,
    TIME_STEPS,
    RANDOM_SEED,
    INIT_POP,
    HUNTING,
    BIRTH_RATES,
    CARRYING_CAPACITY
)
from environment.habitat import LAKE, RIVER, GRASSLAND
from environment.lattice import Lattice
from agents.base_agent import BaseAgent
from core.interactions import resolve_interactions
from core.mortality import apply_mortality
from core.reproduction import apply_reproduction
from core.carrying_capacity import apply_carrying_capacity
from output.animation import Animator
from output.landscape import save_landscape_outputs


OUTPUT_DIR = "output_images"


class Simulation:
    def __init__(self):
        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)

        self.lattice = Lattice(GRID_WIDTH, GRID_HEIGHT, RANDOM_SEED)
        self.agents = []
        self.time = 0

        self.animator = Animator(self.lattice, OUTPUT_DIR)

        self.history = {species: [] for species in INIT_POP.keys()}

        self.kill_history = {
            "IT_on_NT": [],
            "P_on_NT": [],
            "B_on_NT": [],
            "B_on_E": []
        }

        self.birth_history = {species: [] for species in INIT_POP.keys()}

        self.death_history = {
            "age_NT": [],
            "age_IT": [],
            "age_B": [],
            "age_P": [],
            "age_E": [],
            "starve_B": [],
            "starve_P": [],
            "cap_NT": [],
            "cap_IT": [],
            "cap_E": []
        }

        self.initialize_agents()
        self.record_initial_state()

    def initialize_agents(self):
        for species, count in INIT_POP.items():
            created = 0

            while created < count:
                x = np.random.randint(0, GRID_HEIGHT)
                y = np.random.randint(0, GRID_WIDTH)

                agent = BaseAgent(species, x, y)

                if self.lattice.get_habitat(x, y) in agent.allowed_habitats():
                    self.agents.append(agent)
                    created += 1

    def record_initial_state(self):
        self.record()

        for key in self.kill_history:
            self.kill_history[key].append(0)

        for key in self.birth_history:
            self.birth_history[key].append(0)

        for key in self.death_history:
            self.death_history[key].append(0)

    def step(self):
        # 1. Move and age
        for agent in self.agents:
            if agent.alive:
                agent.step(self.lattice, self.agents)

        # 2. Interactions
        kill_stats = resolve_interactions(self.agents, self.lattice, HUNTING)

        # 3. Mortality
        death_stats = apply_mortality(self.agents)

        # 4. Reproduction
        self.agents, birth_stats = apply_reproduction(
            self.agents,
            self.lattice,
            BIRTH_RATES
        )

        # 5. Carrying capacities
        capacity_stats = apply_carrying_capacity(self.agents, CARRYING_CAPACITY)

        for key, value in capacity_stats.items():
            death_stats[key] = value

        # 6. Remove dead agents
        self.agents = [agent for agent in self.agents if agent.alive]

        # 7. Advance time
        self.time += 1

        # 8. Record
        self.record()
        self.record_kills(kill_stats)
        self.record_births(birth_stats)
        self.record_deaths(death_stats)

    def record(self):
        counts = {species: 0 for species in INIT_POP.keys()}

        for agent in self.agents:
            if agent.alive:
                counts[agent.species] += 1

        for species in counts:
            self.history[species].append(counts[species])

        print(
            f"Step {self.time:3d} | "
            + " | ".join([f"{species}={counts[species]}" for species in counts])
        )

    def record_kills(self, kill_stats):
        for key in self.kill_history:
            self.kill_history[key].append(kill_stats.get(key, 0))

    def record_births(self, birth_stats):
        for key in self.birth_history:
            self.birth_history[key].append(birth_stats.get(key, 0))

    def record_deaths(self, death_stats):
        for key in self.death_history:
            self.death_history[key].append(death_stats.get(key, 0))

    def run(self):
        # Capture initial state
        self.animator.capture_frame(self.agents, self.time)

        for _ in range(TIME_STEPS):
            self.step()
            self.animator.capture_frame(self.agents, self.time)

    def ensure_output_dir(self):
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def plot_populations(self):
        self.ensure_output_dir()

        plt.figure(figsize=(10, 6))

        for species, values in self.history.items():
            plt.plot(values, label=species)

        plt.xlabel("time step")
        plt.ylabel("population")
        plt.title("Invasive Species Simulation: Populations")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "populations.png"))
        plt.close()

    def plot_kills(self):
        self.ensure_output_dir()

        plt.figure(figsize=(10, 6))

        for key, values in self.kill_history.items():
            plt.plot(values, label=key)

        plt.xlabel("time step")
        plt.ylabel("kills per step")
        plt.title("Predation Events Over Time")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "kills.png"))
        plt.close()

    def plot_births(self):
        self.ensure_output_dir()

        plt.figure(figsize=(10, 6))

        for key, values in self.birth_history.items():
            plt.plot(values, label=key)

        plt.xlabel("time step")
        plt.ylabel("births per step")
        plt.title("Birth Events Over Time")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "births.png"))
        plt.close()

    def plot_deaths(self):
        self.ensure_output_dir()

        plt.figure(figsize=(10, 6))

        for key, values in self.death_history.items():
            plt.plot(values, label=key)

        plt.xlabel("time step")
        plt.ylabel("deaths per step")
        plt.title("Death Events Over Time")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "deaths.png"))
        plt.close()

    def plot_combined(self):
        self.ensure_output_dir()

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        for key, values in self.history.items():
            axes[0, 0].plot(values, label=key)
        axes[0, 0].set_title("Populations")
        axes[0, 0].set_xlabel("time step")
        axes[0, 0].set_ylabel("population")
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        for key, values in self.kill_history.items():
            axes[0, 1].plot(values, label=key)
        axes[0, 1].set_title("Predation Events")
        axes[0, 1].set_xlabel("time step")
        axes[0, 1].set_ylabel("kills per step")
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        for key, values in self.birth_history.items():
            axes[1, 0].plot(values, label=key)
        axes[1, 0].set_title("Birth Events")
        axes[1, 0].set_xlabel("time step")
        axes[1, 0].set_ylabel("births per step")
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        for key, values in self.death_history.items():
            axes[1, 1].plot(values, label=key)
        axes[1, 1].set_title("Death Events")
        axes[1, 1].set_xlabel("time step")
        axes[1, 1].set_ylabel("deaths per step")
        axes[1, 1].legend()
        axes[1, 1].grid(True)

        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "combined.png"))
        plt.close()

    def plot_spatial_snapshot(self):
        self.ensure_output_dir()

        habitat_cmap = ListedColormap(["#9ecae1", "#3182bd", "#b2df8a"])

        fig, ax = plt.subplots(figsize=(10, 10))

        ax.imshow(
            self.lattice.grid,
            cmap=habitat_cmap,
            origin="upper",
            interpolation="nearest"
        )

        species_style = {
            "IT": {"color": "red", "marker": "s", "label": "Invasive trout"},
            "B": {"color": "black", "marker": "^", "label": "Bear"},
            "P": {"color": "gold", "marker": "*", "label": "Bird"},
            "E": {"color": "darkgreen", "marker": "D", "label": "Elk"}
        }

        # First plot native trout separately by habitat
        nt_lake_x = []
        nt_lake_y = []
        nt_river_x = []
        nt_river_y = []

        for agent in self.agents:
            if not agent.alive or agent.species != "NT":
                continue

            habitat = self.lattice.get_habitat(agent.x, agent.y)
            if habitat == LAKE:
                nt_lake_x.append(agent.y)
                nt_lake_y.append(agent.x)
            elif habitat == RIVER:
                nt_river_x.append(agent.y)
                nt_river_y.append(agent.x)

        if len(nt_lake_x) > 0:
            ax.scatter(
                nt_lake_x,
                nt_lake_y,
                c="orange",
                marker="o",
                s=50,
                label="Native trout (lake)",
                edgecolors="white",
                linewidths=0.5,
                alpha=0.9
            )

        if len(nt_river_x) > 0:
            ax.scatter(
                nt_river_x,
                nt_river_y,
                c="magenta",
                marker="o",
                s=50,
                label="Native trout (river)",
                edgecolors="white",
                linewidths=0.5,
                alpha=0.9
            )

        # Then the remaining species
        for species, style in species_style.items():
            xs = []
            ys = []

            for agent in self.agents:
                if agent.alive and agent.species == species:
                    xs.append(agent.y)
                    ys.append(agent.x)

            if len(xs) > 0:
                ax.scatter(
                    xs,
                    ys,
                    c=style["color"],
                    marker=style["marker"],
                    s=50,
                    label=style["label"],
                    edgecolors="white",
                    linewidths=0.5,
                    alpha=0.9
                )

        ax.set_title(f"Spatial Snapshot at Time Step {self.time}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xticks(range(0, GRID_WIDTH, max(1, GRID_WIDTH // 10)))
        ax.set_yticks(range(0, GRID_HEIGHT, max(1, GRID_HEIGHT // 10)))
        ax.grid(False)
        ax.legend(loc="upper right", fontsize=9)

        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "snapshot.png"))
        plt.close()

    def save_all_plots(self):
        self.plot_populations()
        self.plot_kills()
        self.plot_births()
        self.plot_deaths()
        self.plot_combined()
        self.plot_spatial_snapshot()

        save_landscape_outputs(self.lattice, self.agents)

        print("\nSaved files in output_images/:")
        print(" - populations.png")
        print(" - kills.png")
        print(" - births.png")
        print(" - deaths.png")
        print(" - combined.png")
        print(" - snapshot.png")
        print(" - landscape.png")
        print(" - movement_tendencies.png")
        print(" - density_heatmaps.png")

    def save_animation(self):
        self.animator.save_gif("animation.gif", duration=0.2)