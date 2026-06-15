"""
Plotting utilities for Version B.
"""

import os
import matplotlib.pyplot as plt


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def plot_time_series(history, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(history["step"], history["mean_plant_health"], label="Mean plant health")
    ax.plot(history["step"], history["total_caterpillars"], label="Total caterpillars")
    ax.plot(history["step"], history["mean_defense_level"], label="Mean defense level")
    ax.plot(history["step"], history["day_bloom_fraction"], label="Day-bloom fraction")
    ax.plot(history["step"], history["attacked_fraction"], label="Attacked fraction")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    ax.set_title("Version B: ecosystem time series")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "time_series_version_b.png"), dpi=150)
    plt.close(fig)


def plot_final_health(plant_health, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(plant_health, vmin=0.0, vmax=1.0)
    ax.set_title("Final plant health")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "final_plant_health_version_b.png"), dpi=150)
    plt.close(fig)


def plot_final_defense(defense_level, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(defense_level, vmin=0.0, vmax=1.0)
    ax.set_title("Final defense level")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "final_defense_version_b.png"), dpi=150)
    plt.close(fig)