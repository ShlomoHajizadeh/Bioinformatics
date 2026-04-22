"""
Snapshot utilities for the chase-and-escape simulation
"""

import matplotlib.pyplot as plt


def save_lattice_snapshot(grid, filename, title="Chase and Escape Snapshot"):
    """
    Save a snapshot of the current lattice state.

    Parameters
    ----------
    grid : numpy.ndarray
        2D lattice array.
    filename : str
        Path to the output image file.
    title : str
        Title of the figure.
    """
    plt.figure()
    plt.imshow(grid)
    plt.title(title)
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()