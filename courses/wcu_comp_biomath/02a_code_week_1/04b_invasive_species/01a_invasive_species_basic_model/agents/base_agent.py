
import random
from config.config import MOVES
from environment.habitat import LAKE, RIVER, GRASSLAND


class BaseAgent:
    def __init__(self, species, x, y):
        self.species = species
        self.x = x
        self.y = y
        self.age = 0
        self.alive = True

    def allowed_habitats(self):
        if self.species == "NT":
            return [LAKE, RIVER]
        if self.species == "IT":
            return [LAKE]
        if self.species == "B":
            return [RIVER, GRASSLAND]
        if self.species == "P":
            return [LAKE, RIVER, GRASSLAND]
        if self.species == "E":
            return [GRASSLAND]
        return []

    def move(self, lattice):
        random.shuffle(MOVES)

        for dx, dy in MOVES:
            nx, ny = lattice.wrap(self.x + dx, self.y + dy)
            if lattice.get_habitat(nx, ny) in self.allowed_habitats():
                self.x, self.y = nx, ny
                return

    def step(self, lattice):
        self.move(lattice)
        self.age += 1
