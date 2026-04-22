import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Allow direct execution like: python output/landscape.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment.habitat import LAKE, RIVER, GRASSLAND
from environment.lattice import Lattice
from config.config import GRID_WIDTH, GRID_HEIGHT


OUTPUT_DIR = "output_images"


def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def get_habitat_cmap():
    # lake = light blue, river = darker blue, grassland = light green
    return ListedColormap(["#9ecae1", "#3182bd", "#b2df8a"])


def get_species_display_names():
    return {
        "NT": "Native trout",
        "IT": "Invasive trout",
        "B": "Bear",
        "P": "Bird",
        "E": "Elk"
    }


def get_species_preference_scores():
    """
    Heuristic habitat preferences used to build a movement-tendency vector field.
    These are a visualization aid, not the actual simulation movement rules.
    """
    return {
        "NT": {LAKE: 1.0, RIVER: 0.9, GRASSLAND: 0.0},
        "IT": {LAKE: 1.0, RIVER: 0.0, GRASSLAND: 0.0},
        "B":  {LAKE: 0.0, RIVER: 1.0, GRASSLAND: 0.75},
        "P":  {LAKE: 0.8, RIVER: 0.8, GRASSLAND: 0.8},
        "E":  {LAKE: 0.0, RIVER: 0.0, GRASSLAND: 1.0}
    }


def plot_landscape(lattice, filename="landscape.png"):
    ensure_output_dir()

    cmap = get_habitat_cmap()

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(
        lattice.grid,
        cmap=cmap,
        origin="upper",
        interpolation="nearest"
    )

    ax.set_title("Static Landscape (Lake, River, Grassland)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_xticks(range(0, lattice.width, max(1, lattice.width // 10)))
    ax.set_yticks(range(0, lattice.height, max(1, lattice.height // 10)))
    ax.grid(False)

    legend_elements = [
        Patch(facecolor="#9ecae1", label="Lake"),
        Patch(facecolor="#3182bd", label="River"),
        Patch(facecolor="#b2df8a", label="Grassland")
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path)
    plt.close()

    print(f"Saved landscape: {path}")


def compute_movement_tendency_field(lattice, species):
    """
    Compute a simple local movement-tendency vector field based on habitat desirability.
    """
    scores = get_species_preference_scores()[species]

    U = np.zeros((lattice.height, lattice.width), dtype=float)
    V = np.zeros((lattice.height, lattice.width), dtype=float)

    directions = [
        (-1, 0),   # north
        (0, 1),    # east
        (1, 0),    # south
        (0, -1)    # west
    ]

    for x in range(lattice.height):
        for y in range(lattice.width):
            ux = 0.0
            uy = 0.0

            for dx, dy in directions:
                nx, ny = lattice.wrap(x + dx, y + dy)
                habitat = lattice.get_habitat(nx, ny)
                weight = scores.get(habitat, 0.0)

                ux += weight * dy
                uy += weight * dx

            norm = np.sqrt(ux * ux + uy * uy)
            if norm > 1e-12:
                ux /= norm
                uy /= norm

            U[x, y] = ux
            V[x, y] = uy

    return U, V


def plot_movement_tendency_overlays(lattice, filename="movement_tendencies.png", stride=2):
    ensure_output_dir()

    cmap = get_habitat_cmap()
    display_names = get_species_display_names()
    species_order = ["NT", "IT", "B", "P", "E"]

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    Y, X = np.meshgrid(
        np.arange(lattice.width),
        np.arange(lattice.height)
    )

    for i, species in enumerate(species_order):
        ax = axes[i]

        ax.imshow(
            lattice.grid,
            cmap=cmap,
            origin="upper",
            interpolation="nearest",
            alpha=0.85
        )

        U, V = compute_movement_tendency_field(lattice, species)

        ax.quiver(
            Y[::stride, ::stride],
            X[::stride, ::stride],
            U[::stride, ::stride],
            V[::stride, ::stride],
            color="black",
            scale=20,
            width=0.003
        )

        ax.set_title(display_names[species])
        ax.set_xticks([])
        ax.set_yticks([])

    ax = axes[5]
    ax.axis("off")
    ax.text(0.05, 0.85, "Movement-tendency overlay", fontsize=14, weight="bold")
    ax.text(
        0.05,
        0.62,
        "Arrows indicate local habitat preference\nfor each species.",
        fontsize=11
    )
    ax.text(
        0.05,
        0.42,
        "This is a teaching visualization,\nnot an additional simulation rule.",
        fontsize=11
    )

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path)
    plt.close()

    print(f"Saved movement tendencies: {path}")


def build_species_density_grid(agents, width, height, species):
    density = np.zeros((height, width), dtype=float)

    for agent in agents:
        if agent.alive and agent.species == species:
            density[agent.x, agent.y] += 1.0

    return density


def build_total_density_grid(agents, width, height):
    density = np.zeros((height, width), dtype=float)

    for agent in agents:
        if agent.alive:
            density[agent.x, agent.y] += 1.0

    return density


def plot_species_density_heatmaps(lattice, agents, filename="density_heatmaps.png"):
    ensure_output_dir()

    habitat_cmap = get_habitat_cmap()
    display_names = get_species_display_names()
    species_order = ["NT", "IT", "B", "P", "E"]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for i, species in enumerate(species_order):
        ax = axes[i]

        density = build_species_density_grid(agents, lattice.width, lattice.height, species)
        masked_density = np.ma.masked_where(density <= 0, density)

        ax.imshow(
            lattice.grid,
            cmap=habitat_cmap,
            origin="upper",
            interpolation="nearest",
            alpha=0.55
        )

        im = ax.imshow(
            masked_density,
            cmap="Reds",
            origin="upper",
            interpolation="nearest",
            alpha=0.85
        )

        ax.set_title(f"{display_names[species]} density")
        ax.set_xticks([])
        ax.set_yticks([])

        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("count per cell")

    ax = axes[5]
    density = build_total_density_grid(agents, lattice.width, lattice.height)
    masked_density = np.ma.masked_where(density <= 0, density)

    ax.imshow(
        lattice.grid,
        cmap=habitat_cmap,
        origin="upper",
        interpolation="nearest",
        alpha=0.55
    )

    im = ax.imshow(
        masked_density,
        cmap="Reds",
        origin="upper",
        interpolation="nearest",
        alpha=0.85
    )

    ax.set_title("Total occupancy density")
    ax.set_xticks([])
    ax.set_yticks([])

    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("count per cell")

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path)
    plt.close()

    print(f"Saved density heatmaps: {path}")


def save_landscape_outputs(lattice, agents=None):
    """
    Save all landscape-related outputs.
    """
    plot_landscape(lattice)
    plot_movement_tendency_overlays(lattice)

    if agents is not None:
        plot_species_density_heatmaps(lattice, agents)


def main():
    lattice = Lattice(GRID_WIDTH, GRID_HEIGHT)
    save_landscape_outputs(lattice)


if __name__ == "__main__":
    main()