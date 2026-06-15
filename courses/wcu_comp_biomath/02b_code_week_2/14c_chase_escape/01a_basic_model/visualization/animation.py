"""
Animation utilities for the chase-and-escape simulation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap, BoundaryNorm


def _get_cmap():
    """
    Discrete colormap:
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

    ax.set_xlim(-0.5, ny - 0.5)
    ax.set_ylim(nx - 0.5, -0.5)

    ax.set_xticks([x - 0.5 for x in range(ny + 1)])
    ax.set_yticks([y - 0.5 for y in range(nx + 1)])

    ax.grid(color="black", linewidth=0.5)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)

    ax.set_aspect("equal")


def animate_simulation(
    history_grids,
    interval=200,
    title="Chase-and-Escape Animation",
    show=True,
):
    """
    Create an animation from a sequence of lattice states.

    Parameters
    ----------
    history_grids : list of numpy.ndarray
        List of 2D lattice states.
    interval : int
        Delay between frames in milliseconds.
    title : str
        Base title for the animation.
    show : bool
        If True, display the animation window.

    Returns
    -------
    anim : matplotlib.animation.FuncAnimation
        Animation object.
    """
    if len(history_grids) == 0:
        raise ValueError("history_grids is empty")

    cmap, norm = _get_cmap()

    fig, ax = plt.subplots()

    im = ax.imshow(
        history_grids[0],
        cmap=cmap,
        norm=norm,
        interpolation="none",
        animated=True,
    )

    ax.set_title(f"{title} (step 0)")
    ax.set_xlabel("y")
    ax.set_ylabel("x")

    _format_lattice_axes(ax, history_grids[0].shape)

    legend_patches = [
        mpatches.Patch(facecolor="white", edgecolor="black", label="Empty"),
        mpatches.Patch(facecolor="green", edgecolor="black", label="Target"),
        mpatches.Patch(facecolor="red", edgecolor="black", label="Chaser"),
    ]
    ax.legend(handles=legend_patches, loc="upper right")

    def update(frame):
        im.set_array(history_grids[frame])
        ax.set_title(f"{title} (step {frame})")
        return [im]

    anim = FuncAnimation(
        fig,
        update,
        frames=len(history_grids),
        interval=interval,
        blit=False,
        repeat=False,
    )

    if show:
        plt.show()

    return anim


def save_animation_gif(anim, filename="animation.gif", fps=5):
    """
    Save animation as GIF using Pillow.

    Parameters
    ----------
    anim : matplotlib.animation.FuncAnimation
    filename : str
    fps : int
    """
    writer = PillowWriter(fps=fps)
    anim.save(filename, writer=writer)
    print(f"Animation saved as GIF: {filename}")