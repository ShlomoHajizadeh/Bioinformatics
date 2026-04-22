import numpy as np


class Environment3D:
    def __init__(self, x_size: float, y_size: float, z_size: float, periodic: bool = True):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.periodic = periodic

    def domain_lengths(self) -> np.ndarray:
        return np.array([self.x_size, self.y_size, self.z_size], dtype=float)

    def apply_boundaries(self, position: np.ndarray, velocity: np.ndarray):
        if self.periodic:
            position[0] = position[0] % self.x_size
            position[1] = position[1] % self.y_size
            position[2] = position[2] % self.z_size
            return position, velocity

        # reflecting boundaries
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