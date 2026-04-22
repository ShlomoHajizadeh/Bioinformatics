from enum import Enum


class SexType(Enum):
    MALE = "male"
    FEMALE = "female"
    HERMAPHRODITE = "hermaphrodite"


class LifeStage(Enum):
    JUVENILE = "juvenile"
    ADULT = "adult"
    REPRODUCTIVE_ADULT = "reproductive_adult"