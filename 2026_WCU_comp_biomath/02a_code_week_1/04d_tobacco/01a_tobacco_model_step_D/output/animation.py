"""
Animation for Version D.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def build_rgb_image(plant_health, defense_level, signal, predator_attractant):
    h, w = plant_health.shape
    img = np.zeros((h, w, 3), dtype=float)

    healthy = plant_health > 0.7
    mid = (plant_health > 0.3) & (plant_health <= 0.7)
    low = plant_health <= 0.3
    defended = defense_level > 0.05

    img[healthy] = np.array([0.20, 0.70, 0.20])
    img[mid] = np.array([0.60, 0.50, 0.20])
    img[low] = np.array([0.30, 0.30, 0.30])
    img[defended] = np.array([0.95, 0.55, 0.15])

    # signal reddens slightly; attractant brightens blue slightly
    img[..., 0] = np.clip(img[..., 0] + 0.30 * signal, 0.0, 1.0)
    img[..., 2] = np.clip(img[..., 2] + 0.30 * predator_attractant, 0.0, 1.0)

    return img


def create_animation(frames, output_dir, gif_name="tobacco_version_d.gif", interval=200):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(7, 7))
    first = frames[0]

    rgb = build_rgb_image(
        first["plant_health"],
        first["defense_level"],
        first["signal"],
        first["predator_attractant"],
    )
    im = ax.imshow(rgb)

    moth_scatter = ax.scatter(first["moth_x"], first["moth_y"], s=20)
    pred_scatter = ax.scatter(first["pred_x"], first["pred_y"], s=30, marker="x")
    cat_scatter = ax.scatter([], [], s=12, marker="s")

    def update(frame):
        rgb = build_rgb_image(
            frame["plant_health"],
            frame["defense_level"],
            frame["signal"],
            frame["predator_attractant"],
        )
        caterpillars = frame["caterpillars"]
        im.set_data(rgb)

        moth_scatter.set_offsets(np.column_stack((frame["moth_x"], frame["moth_y"])))
        pred_scatter.set_offsets(np.column_stack((frame["pred_x"], frame["pred_y"])))

        ys, xs = np.where(caterpillars > 0)
        cat_offsets = np.column_stack((xs, ys)) if len(xs) > 0 else np.empty((0, 2))
        cat_scatter.set_offsets(cat_offsets)

        ax.set_title(
            f"Step {frame['step']} | {frame['phase']} | "
            f"Caterpillars: {int(caterpillars.sum())} | "
            f"Defense: {frame['defense_level'].mean():.2f} | "
            f"Attractant: {frame['predator_attractant'].mean():.2f}"
        )
        return im, moth_scatter, pred_scatter, cat_scatter

    anim = FuncAnimation(fig, update, frames=frames, interval=interval, blit=False)
    gif_path = os.path.join(output_dir, gif_name)
    anim.save(gif_path, writer=PillowWriter(fps=5))
    plt.close(fig)
    return gif_path