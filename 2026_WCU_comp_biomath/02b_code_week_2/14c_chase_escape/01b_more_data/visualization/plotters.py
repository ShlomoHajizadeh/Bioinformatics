"""
Simple plotting utilities
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, BoundaryNorm


def _get_cmap():
    """
    Create a discrete colormap:
    0 = empty (white)
    1 = target (green)
    2 = chaser (red)
    """
    cmap = ListedColormap(["white", "green", "red"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)
    return cmap, norm


def _format_lattice_axes(ax, shape):
    """
    Format axes so that grid lines appear along cell boundaries.
    """
    nx, ny = shape

    # Make sure the image occupies exactly the lattice rectangle
    ax.set_xlim(-0.5, ny - 0.5)
    ax.set_ylim(nx - 0.5, -0.5)

    # Put ticks on cell boundaries
    ax.set_xticks([x - 0.5 for x in range(ny + 1)])
    ax.set_yticks([y - 0.5 for y in range(nx + 1)])

    # Draw grid on those boundary ticks
    ax.grid(color="black", linewidth=0.5)

    # Hide tick labels and tick marks
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)

    ax.set_aspect("equal")


def plot_lattice(grid):
    """
    Plot one lattice state with explicit colors and visible grid lines.
    """
    cmap, norm = _get_cmap()

    fig, ax = plt.subplots()
    ax.imshow(grid, cmap=cmap, norm=norm, interpolation="none")

    ax.set_title("Chase and Escape (final state)")
    ax.set_xlabel("y")
    ax.set_ylabel("x")

    _format_lattice_axes(ax, grid.shape)

    legend_patches = [
        mpatches.Patch(facecolor="white", edgecolor="black", label="Empty"),
        mpatches.Patch(facecolor="green", edgecolor="black", label="Target"),
        mpatches.Patch(facecolor="red", edgecolor="black", label="Chaser"),
    ]
    ax.legend(handles=legend_patches, loc="upper right")

    plt.show()


def plot_targets(history):
    """
    Plot number of surviving targets over time.
    """
    fig, ax = plt.subplots()
    ax.plot(history)
    ax.set_xlabel("Time")
    ax.set_ylabel("Number of targets")
    ax.set_title("Target survival over time")
    plt.show()