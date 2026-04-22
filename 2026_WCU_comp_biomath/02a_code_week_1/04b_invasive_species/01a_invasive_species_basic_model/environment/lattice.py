
import numpy as np
from environment.habitat import LAKE, RIVER, GRASSLAND


class Lattice:
    def __init__(self, width, height, seed=42):
        np.random.seed(seed)
        self.width = width
        self.height = height

        # Simple random habitat map
        self.grid = np.random.choice(
            [LAKE, RIVER, GRASSLAND],
            size=(height, width),
            p=[0.4, 0.2, 0.4]
        )

    def wrap(self, x, y):
        return x % self.height, y % self.width

    def get_habitat(self, x, y):
        return self.grid[x, y]