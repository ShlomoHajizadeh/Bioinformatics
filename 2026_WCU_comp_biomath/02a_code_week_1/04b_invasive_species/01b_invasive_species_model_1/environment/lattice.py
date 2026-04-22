import numpy as np

from environment.habitat import LAKE, RIVER, GRASSLAND


class Lattice:
    def __init__(self, width, height, seed=42):
        self.width = width
        self.height = height
        self.seed = seed

        # Start with all grassland
        self.grid = np.full((height, width), GRASSLAND, dtype=int)

        # Build a static, ecologically more realistic landscape
        self.create_static_landscape()

    def wrap(self, x, y):
        return x % self.height, y % self.width

    def get_habitat(self, x, y):
        return self.grid[x, y]

    def create_static_landscape(self):
        """
        Create a static habitat map with:
        - a large lake in the upper-right / upper-middle region
        - a river flowing downward out of the lake
        - toroidal continuity through wrapping
        - connected grassland elsewhere
        """
        self.grid[:, :] = GRASSLAND

        self.add_lake()
        self.add_river_from_lake_outlet()

    def add_lake(self):
        """
        Add one broad lake as a union of overlapping ellipses.
        """
        lake_parts = [
            # (center_x, center_y, radius_x, radius_y)
            (int(0.16 * self.height), int(0.70 * self.width),
             max(4, int(0.14 * self.height)), max(6, int(0.16 * self.width))),
            (int(0.16 * self.height), int(0.84 * self.width),
             max(4, int(0.13 * self.height)), max(5, int(0.13 * self.width))),
            (int(0.22 * self.height), int(0.60 * self.width),
             max(3, int(0.10 * self.height)), max(4, int(0.10 * self.width))),
        ]

        for x in range(self.height):
            for y in range(self.width):
                for cx, cy, rx, ry in lake_parts:
                    dx = (x - cx) / rx
                    dy = (y - cy) / ry
                    if dx * dx + dy * dy <= 1.0:
                        self.grid[x, y] = LAKE
                        break

    def find_lake_outlet_start_row(self, outlet_col):
        """
        Find the lowest lake row near the outlet column.
        The river should start below this row.
        """
        search_cols = [
            outlet_col - 1,
            outlet_col,
            outlet_col + 1
        ]

        lowest_lake_row = -1

        for x in range(self.height):
            for y in search_cols:
                yy = y % self.width
                if self.grid[x, yy] == LAKE:
                    if x > lowest_lake_row:
                        lowest_lake_row = x

        # Start river one row below the lowest lake cell near the outlet
        return min(self.height - 1, lowest_lake_row + 1)

    def add_river_from_lake_outlet(self):
        """
        Add a river that starts below the lake rather than cutting through it.
        """
        base_col = int(0.68 * self.width)
        half_width = max(1, int(0.03 * self.width))

        start_row = self.find_lake_outlet_start_row(base_col)

        # Add a small outlet neck just below the lake
        for x in range(start_row, min(self.height, start_row + 2)):
            for d in range(-1, 2):
                y = (base_col + d) % self.width
                # Only place river outside the lake body
                if self.grid[x, y] != LAKE:
                    self.grid[x, y] = RIVER

        # Main river starts below the lake outlet
        for x in range(start_row + 1, self.height):
            offset = int(2.0 * np.sin(2.0 * np.pi * (x - start_row) / self.height))
            center_col = (base_col + offset) % self.width

            for d in range(-half_width, half_width + 1):
                y = (center_col + d) % self.width
                self.grid[x, y] = RIVER

        # Optional toroidal continuation near the top boundary,
        # but do not overwrite the lake.
        for x in range(0, 1):
            offset = int(2.0 * np.sin(2.0 * np.pi * (x - start_row) / self.height))
            center_col = (base_col + offset) % self.width

            for d in range(-half_width, half_width + 1):
                y = (center_col + d) % self.width
                if self.grid[x, y] != LAKE:
                    self.grid[x, y] = RIVER