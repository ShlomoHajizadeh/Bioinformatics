import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import imageio

from environment.habitat import LAKE, RIVER


class Animator:
    def __init__(self, lattice, output_dir="output_images"):
        self.lattice = lattice
        self.frames = []
        self.output_dir = output_dir

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def capture_frame(self, agents, time_step):
        """
        Capture the current spatial state as one animation frame.
        Native trout are visually separated into:
        - orange: native trout in lake
        - magenta: native trout in river
        """
        habitat_cmap = ListedColormap(["#9ecae1", "#3182bd", "#b2df8a"])

        fig, ax = plt.subplots(figsize=(6, 6))

        # Draw habitat background
        ax.imshow(
            self.lattice.grid,
            cmap=habitat_cmap,
            origin="upper",
            interpolation="nearest"
        )

        # Native trout split by habitat
        nt_lake_x = []
        nt_lake_y = []
        nt_river_x = []
        nt_river_y = []

        for agent in agents:
            if not agent.alive or agent.species != "NT":
                continue

            habitat = self.lattice.get_habitat(agent.x, agent.y)
            if habitat == LAKE:
                nt_lake_x.append(agent.y)
                nt_lake_y.append(agent.x)
            elif habitat == RIVER:
                nt_river_x.append(agent.y)
                nt_river_y.append(agent.x)

        if nt_lake_x:
            ax.scatter(
                nt_lake_x,
                nt_lake_y,
                c="orange",
                marker="o",
                s=28,
                alpha=0.85,
                edgecolors="white",
                linewidths=0.25,
                label="NT lake"
            )

        if nt_river_x:
            ax.scatter(
                nt_river_x,
                nt_river_y,
                c="magenta",
                marker="o",
                s=28,
                alpha=0.85,
                edgecolors="white",
                linewidths=0.25,
                label="NT river"
            )

        # Remaining species
        species_style = {
            "IT": {"color": "red", "marker": "s", "label": "IT"},
            "B": {"color": "black", "marker": "^", "label": "B"},
            "P": {"color": "gold", "marker": "*", "label": "P"},
            "E": {"color": "darkgreen", "marker": "D", "label": "E"}
        }

        for species, style in species_style.items():
            xs = []
            ys = []

            for agent in agents:
                if agent.alive and agent.species == species:
                    xs.append(agent.y)
                    ys.append(agent.x)

            if xs:
                ax.scatter(
                    xs,
                    ys,
                    c=style["color"],
                    marker=style["marker"],
                    s=28,
                    alpha=0.85,
                    edgecolors="white",
                    linewidths=0.25,
                    label=style["label"]
                )

        ax.set_title(f"Spatial dynamics at t = {time_step}")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.legend(loc="upper right", fontsize=7)

        fig.tight_layout()
        fig.canvas.draw()

        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        image = image[:, :, :3].copy()

        self.frames.append(image)

        plt.close(fig)

    def save_gif(self, filename="animation.gif", duration=0.2):
        """
        Save all captured frames as an animated GIF.
        """
        path = os.path.join(self.output_dir, filename)
        imageio.mimsave(path, self.frames, duration=duration)
        print(f"\nSaved animation: {path}")