import random

from config.config import MOVES, SENSING_RADIUS
from environment.habitat import LAKE, RIVER, GRASSLAND


class BaseAgent:
    def __init__(self, species, x, y):
        self.species = species
        self.x = x
        self.y = y
        self.age = 0
        self.alive = True

        # Feeding counters
        self.steps_since_nt_meal = 0
        self.steps_since_bear_nt_meal = 0
        self.steps_since_bear_e_meal = 0

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

    def torus_distance(self, x1, y1, x2, y2, lattice):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        dx = min(dx, lattice.height - dx)
        dy = min(dy, lattice.width - dy)

        return dx + dy

    def count_species_near(self, x, y, agents, target_species, lattice, allowed_habitats=None):
        count = 0

        for agent in agents:
            if not agent.alive:
                continue
            if agent.species != target_species:
                continue

            if allowed_habitats is not None:
                if lattice.get_habitat(agent.x, agent.y) not in allowed_habitats:
                    continue

            d = self.torus_distance(x, y, agent.x, agent.y, lattice)
            if d <= SENSING_RADIUS:
                count += 1

        return count

    def score_position(self, x, y, lattice, agents):
        habitat = lattice.get_habitat(x, y)

        if habitat not in self.allowed_habitats():
            return -10**9

        score = 0.0

        # Native trout:
        # prefer lake/river with NT-friendly habitats,
        # but if invasive trout are nearby in lake, shift toward river.
        if self.species == "NT":
            if habitat == LAKE:
                score += 4.0
            if habitat == RIVER:
                score += 5.0

            nearby_it = self.count_species_near(x, y, agents, "IT", lattice, allowed_habitats=[LAKE])
            nearby_nt = self.count_species_near(x, y, agents, "NT", lattice)

            score += 0.3 * nearby_nt

            if habitat == LAKE:
                score -= 2.5 * nearby_it
            if habitat == RIVER:
                score += 1.5 * nearby_it

        # Invasive trout:
        # remain in lake and seek native trout there.
        elif self.species == "IT":
            if habitat == LAKE:
                score += 6.0

            nearby_nt_lake = self.count_species_near(x, y, agents, "NT", lattice, allowed_habitats=[LAKE])
            score += 2.0 * nearby_nt_lake

        # Birds:
        # can move everywhere, but should strongly prefer lake zones with native trout.
        # This keeps them feeding while NT are still in the lake.
        elif self.species == "P":
            if habitat == LAKE:
                score += 6.0
            elif habitat == RIVER:
                score += 1.0
            elif habitat == GRASSLAND:
                score += 0.5

            nearby_nt_lake = self.count_species_near(x, y, agents, "NT", lattice, allowed_habitats=[LAKE])
            score += 2.5 * nearby_nt_lake

            # slight penalty for drifting away from water-rich zones
            if habitat == GRASSLAND:
                score -= 1.0

        # Bears:
        # prefer river trout first; if trout are scarce, shift toward elk in grassland.
        elif self.species == "B":
            nearby_nt_river = self.count_species_near(x, y, agents, "NT", lattice, allowed_habitats=[RIVER])
            nearby_elk = self.count_species_near(x, y, agents, "E", lattice, allowed_habitats=[GRASSLAND])

            if habitat == RIVER:
                score += 4.0
            if habitat == GRASSLAND:
                score += 2.0

            # Primary target: native trout in river
            score += 2.5 * nearby_nt_river

            # If no recent trout meal, elk become increasingly attractive
            if self.steps_since_bear_nt_meal > 4:
                score += 1.8 * nearby_elk
                if habitat == GRASSLAND:
                    score += 1.0

        # Elk:
        # stay in grassland, weakly prefer other elk.
        elif self.species == "E":
            if habitat == GRASSLAND:
                score += 5.0

            nearby_elk = self.count_species_near(x, y, agents, "E", lattice, allowed_habitats=[GRASSLAND])
            score += 0.4 * nearby_elk

        return score

    def move(self, lattice, agents):
        candidates = []

        for dx, dy in MOVES:
            nx, ny = lattice.wrap(self.x + dx, self.y + dy)

            if lattice.get_habitat(nx, ny) in self.allowed_habitats():
                score = self.score_position(nx, ny, lattice, agents)
                candidates.append((score, nx, ny))

        if len(candidates) == 0:
            return

        max_score = max(c[0] for c in candidates)
        best = [c for c in candidates if c[0] == max_score]

        _, nx, ny = random.choice(best)
        self.x = nx
        self.y = ny

    def step(self, lattice, agents):
        self.move(lattice, agents)
        self.age += 1

        if self.species == "P":
            self.steps_since_nt_meal += 1

        if self.species == "B":
            self.steps_since_bear_nt_meal += 1
            self.steps_since_bear_e_meal += 1