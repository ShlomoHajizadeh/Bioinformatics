import numpy as np


class Environment3D:
    def __init__(
        self,
        x_size: float,
        y_size: float,
        z_size: float,
        periodic: bool = True,
        grid_shape=(16, 16, 16),
        initial_nutrient_level: float = 1.0,
    ):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.periodic = periodic

        self.grid_nx, self.grid_ny, self.grid_nz = grid_shape

        self.nutrients = np.full(
            (self.grid_nx, self.grid_ny, self.grid_nz),
            fill_value=initial_nutrient_level,
            dtype=float,
        )
        self.pheromones = np.zeros(
            (self.grid_nx, self.grid_ny, self.grid_nz),
            dtype=float,
        )

        self.dx = self.x_size / self.grid_nx
        self.dy = self.y_size / self.grid_ny
        self.dz = self.z_size / self.grid_nz

    def domain_lengths(self) -> np.ndarray:
        return np.array([self.x_size, self.y_size, self.z_size], dtype=float)

    def apply_boundaries(self, position: np.ndarray, velocity: np.ndarray):
        if self.periodic:
            position[0] = position[0] % self.x_size
            position[1] = position[1] % self.y_size
            position[2] = position[2] % self.z_size
            return position, velocity

        if position[0] < 0:
            position[0] = -position[0]
            velocity[0] *= -1
        elif position[0] > self.x_size:
            position[0] = 2 * self.x_size - position[0]
            velocity[0] *= -1

        if position[1] < 0:
            position[1] = -position[1]
            velocity[1] *= -1
        elif position[1] > self.y_size:
            position[1] = 2 * self.y_size - position[1]
            velocity[1] *= -1

        if position[2] < 0:
            position[2] = -position[2]
            velocity[2] *= -1
        elif position[2] > self.z_size:
            position[2] = 2 * self.z_size - position[2]
            velocity[2] *= -1

        return position, velocity

    def displacement(self, pos_a: np.ndarray, pos_b: np.ndarray) -> np.ndarray:
        d = pos_b - pos_a
        if self.periodic:
            lengths = self.domain_lengths()
            for k in range(3):
                if d[k] > 0.5 * lengths[k]:
                    d[k] -= lengths[k]
                elif d[k] < -0.5 * lengths[k]:
                    d[k] += lengths[k]
        return d

    def distance(self, pos_a: np.ndarray, pos_b: np.ndarray) -> float:
        return np.linalg.norm(self.displacement(pos_a, pos_b))

    def position_to_index(self, position: np.ndarray):
        ix = min(self.grid_nx - 1, max(0, int(position[0] / self.dx)))
        iy = min(self.grid_ny - 1, max(0, int(position[1] / self.dy)))
        iz = min(self.grid_nz - 1, max(0, int(position[2] / self.dz)))
        return ix, iy, iz

    def get_local_nutrient(self, position: np.ndarray) -> float:
        ix, iy, iz = self.position_to_index(position)
        return float(self.nutrients[ix, iy, iz])

    def get_local_pheromone(self, position: np.ndarray) -> float:
        ix, iy, iz = self.position_to_index(position)
        return float(self.pheromones[ix, iy, iz])

    def consume_nutrient(self, position: np.ndarray, amount: float) -> float:
        ix, iy, iz = self.position_to_index(position)
        available = self.nutrients[ix, iy, iz]
        consumed = min(available, amount)
        self.nutrients[ix, iy, iz] -= consumed
        return float(consumed)

    def deposit_pheromone(self, position: np.ndarray, amount: float) -> None:
        ix, iy, iz = self.position_to_index(position)
        self.pheromones[ix, iy, iz] += amount

    def pheromone_gradient(self, position: np.ndarray) -> np.ndarray:
        ix, iy, iz = self.position_to_index(position)

        def neighbor_index(i, n, step):
            j = i + step
            if self.periodic:
                return j % n
            return min(n - 1, max(0, j))

        im = neighbor_index(ix, self.grid_nx, -1)
        ip = neighbor_index(ix, self.grid_nx, +1)
        jm = neighbor_index(iy, self.grid_ny, -1)
        jp = neighbor_index(iy, self.grid_ny, +1)
        km = neighbor_index(iz, self.grid_nz, -1)
        kp = neighbor_index(iz, self.grid_nz, +1)

        gx = (self.pheromones[ip, iy, iz] - self.pheromones[im, iy, iz]) / (2.0 * self.dx)
        gy = (self.pheromones[ix, jp, iz] - self.pheromones[ix, jm, iz]) / (2.0 * self.dy)
        gz = (self.pheromones[ix, iy, kp] - self.pheromones[ix, iy, km]) / (2.0 * self.dz)

        return np.array([gx, gy, gz], dtype=float)

    def regenerate_nutrients(self, regen_rate: float, nutrient_max: float) -> None:
        self.nutrients += regen_rate * (nutrient_max - self.nutrients)
        self.nutrients = np.clip(self.nutrients, 0.0, nutrient_max)

    def diffuse_and_decay_pheromones(
        self,
        diffusion_strength: float,
        decay_rate: float,
        pheromone_max: float,
    ) -> None:
        p = self.pheromones

        if self.periodic:
            neighbor_sum = (
                np.roll(p, 1, axis=0) + np.roll(p, -1, axis=0) +
                np.roll(p, 1, axis=1) + np.roll(p, -1, axis=1) +
                np.roll(p, 1, axis=2) + np.roll(p, -1, axis=2)
            )
        else:
            padded = np.pad(p, 1, mode="edge")
            neighbor_sum = (
                padded[:-2, 1:-1, 1:-1] + padded[2:, 1:-1, 1:-1] +
                padded[1:-1, :-2, 1:-1] + padded[1:-1, 2:, 1:-1] +
                padded[1:-1, 1:-1, :-2] + padded[1:-1, 1:-1, 2:]
            )

        laplacian = neighbor_sum - 6.0 * p
        self.pheromones = p + diffusion_strength * laplacian - decay_rate * p
        self.pheromones = np.clip(self.pheromones, 0.0, pheromone_max)

    def mean_nutrient(self) -> float:
        return float(np.mean(self.nutrients))

    def mean_pheromone(self) -> float:
        return float(np.mean(self.pheromones))