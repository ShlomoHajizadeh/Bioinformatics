from dataclasses import dataclass, field
import numpy as np

from core.enums import SexType, LifeStage


@dataclass
class NematodeAgent:
    agent_id: int
    sex_type: SexType
    life_stage: LifeStage
    position: np.ndarray
    velocity: np.ndarray
    age: float = 0.0
    alive: bool = True
    stress_level: float = 0.0
    fertilized_by_male: bool = False
    time_since_last_birth: float = 0.0

    def is_reproductive(self) -> bool:
        return self.life_stage == LifeStage.REPRODUCTIVE_ADULT and self.alive

    def can_mate(self) -> bool:
        return self.alive and self.life_stage in {
            LifeStage.ADULT,
            LifeStage.REPRODUCTIVE_ADULT,
        }

    def can_give_birth(self) -> bool:
        return self.is_reproductive()

    def step_birth_clock(self, dt: float) -> None:
        self.time_since_last_birth += dt

    def reset_birth_clock(self) -> None:
        self.time_since_last_birth = 0.0

    def ready_to_reproduce(self, cooldown: float) -> bool:
        return self.time_since_last_birth >= cooldown

    def copy_position(self) -> np.ndarray:
        return self.position.copy()

    def copy_velocity(self) -> np.ndarray:
        return self.velocity.copy()