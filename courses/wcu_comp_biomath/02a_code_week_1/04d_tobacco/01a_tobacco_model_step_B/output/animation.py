"""
Animation for Version B.

Plant coloring:
- healthy, undefended plant: green
- defended plant: orange
- very damaged plant: brownish
- dead plant: dark gray

Overlay:
- blue dots = moths
- red squares = cells with caterpillars
- black x = predators
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def build_rgb_image(plant_health, defense_level):
    """
    Build a custom RGB image from plant state.
    """
    h, w = plant_health.shape
    img = np.zeros((h, w, 3), dtype=float)

    healthy = plant_health > 0.7
    mid = (plant_health > 0.3) & (plant_health <= 0.7)
    low = plant_health <= 0.3
    defended = defense_level > 0.05

    img[healthy] = np.array([0.2, 0.7, 0.2])   # green
    img[mid] = np.array([0.6, 0.5, 0.2])       # olive/brown
    img[low] = np.array([0.3, 0.3, 0.3])       # dark gray

    # defended plants become orange-ish
    img[defended] = np.array([0.95, 0.55, 0.15])

    return img


def create_animation(frames, output_dir, gif_name="tobacco_version_b.gif", interval=200):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(7, 7))

    first = frames[0]
    rgb = build_rgb_image(first["plant_health"], first["defense_level"])
    im = ax.imshow(rgb)

    moth_scatter = ax.scatter(first["moth_x"], first["moth_y"], s=20)
    pred_scatter = ax.scatter(first["pred_x"], first["pred_y"], s=30, marker="x")
    cat_scatter = ax.scatter([], [], s=12, marker="s")

    ax.set_title("Tobacco ecosystem Version B")

    def update(frame):
        rgb = build_rgb_image(frame["plant_health"], frame["defense_level"])
        caterpillars = frame["caterpillars"]

        im.set_data(rgb)

        moth_offsets = np.column_stack((frame["moth_x"], frame["moth_y"]))
        pred_offsets = np.column_stack((frame["pred_x"], frame["pred_y"]))
        moth_scatter.set_offsets(moth_offsets)
        pred_scatter.set_offsets(pred_offsets)

        ys, xs = np.where(caterpillars > 0)
        if len(xs) > 0:
            cat_offsets = np.column_stack((xs, ys))
        else:
            cat_offsets = np.empty((0, 2))
        cat_scatter.set_offsets(cat_offsets)

        ax.set_title(
            f"Step {frame['step']} | {frame['phase']} | "
            f"Caterpillars: {int(caterpillars.sum())} | "
            f"Mean defense: {frame['defense_level'].mean():.2f}"
        )

        return im, moth_scatter, pred_scatter, cat_scatter

    anim = FuncAnimation(fig, update, frames=frames, interval=interval, blit=False)
    gif_path = os.path.join(output_dir, gif_name)
    anim.save(gif_path, writer=PillowWriter(fps=5))
    plt.close(fig)
    return gif_path