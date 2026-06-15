"""
Plotting utilities for Version C.
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
    ax.plot(history["step"], history["mean_defense_level"], label="Mean defense")
    ax.plot(history["step"], history["mean_signal"], label="Mean signal")
    ax.plot(history["step"], history["mean_priming"], label="Mean priming")
    ax.plot(history["step"], history["day_bloom_fraction"], label="Day-bloom fraction")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    ax.set_title("Version C: ecosystem time series")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "time_series_version_c.png"), dpi=150)
    plt.close(fig)


def plot_final_health(plant_health, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(plant_health, vmin=0.0, vmax=1.0)
    ax.set_title("Final plant health")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "final_plant_health_version_c.png"), dpi=150)
    plt.close(fig)


def plot_final_defense(defense_level, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(defense_level, vmin=0.0, vmax=1.0)
    ax.set_title("Final defense level")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "final_defense_version_c.png"), dpi=150)
    plt.close(fig)


def plot_final_signal(signal, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(signal, vmin=0.0, vmax=1.0)
    ax.set_title("Final volatile signal")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "final_signal_version_c.png"), dpi=150)
    plt.close(fig)