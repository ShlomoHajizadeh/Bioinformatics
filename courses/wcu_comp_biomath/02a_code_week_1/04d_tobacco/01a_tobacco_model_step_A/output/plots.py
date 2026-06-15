"""
Plotting utilities for Version A.
"""

import os
import matplotlib.pyplot as plt
import numpy as np


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def plot_time_series(history, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(history["step"], history["mean_plant_health"], label="Mean plant health")
    ax.plot(history["step"], history["total_eggs"], label="Total eggs")
    ax.plot(history["step"], history["total_caterpillars"], label="Total caterpillars")
    ax.plot(history["step"], history["total_predation"], label="Total predation")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    ax.set_title("Version A: ecosystem time series")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "time_series.png"), dpi=150)
    plt.close(fig)


def plot_final_health(plant_health, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(plant_health, vmin=0.0, vmax=1.0)
    ax.set_title("Final plant health")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "final_plant_health.png"), dpi=150)
    plt.close(fig)


def plot_final_caterpillars(caterpillars, output_dir):
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(caterpillars)
    ax.set_title("Final caterpillar counts")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "final_caterpillars.png"), dpi=150)
    plt.close(fig)