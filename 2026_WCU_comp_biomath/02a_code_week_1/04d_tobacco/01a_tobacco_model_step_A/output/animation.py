"""
Animation for Version A.

Plants are shown as a green-to-brown map:
- healthy plants are greener
- damaged plants are darker/browner via the chosen colormap

Overlay:
- blue dots = moths
- red dots = caterpillars (cells with caterpillars)
- black x = predators
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def create_animation(frames, output_dir, gif_name="tobacco_version_a.gif", interval=200):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(7, 7))

    first = frames[0]
    im = ax.imshow(first["plant_health"], vmin=0.0, vmax=1.0, cmap="YlGn")
    moth_scatter = ax.scatter(first["moth_x"], first["moth_y"], s=20)
    pred_scatter = ax.scatter(first["pred_x"], first["pred_y"], s=30, marker="x")
    cat_scatter = ax.scatter([], [], s=12, marker="s")

    ax.set_title("Tobacco ecosystem Version A")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    def update(frame):
        plant_health = frame["plant_health"]
        caterpillars = frame["caterpillars"]

        im.set_data(plant_health)

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
            f"Caterpillars: {int(caterpillars.sum())}"
        )

        return im, moth_scatter, pred_scatter, cat_scatter

    anim = FuncAnimation(fig, update, frames=frames, interval=interval, blit=False)
    gif_path = os.path.join(output_dir, gif_name)
    anim.save(gif_path, writer=PillowWriter(fps=5))
    plt.close(fig)
    return gif_path