from dataclasses import dataclass


@dataclass
class SimulationConfig:
    # -----------------------------
    # Randomness
    # -----------------------------
    RANDOM_SEED: int = 42

    # -----------------------------
    # Time settings
    # -----------------------------
    DT: float = 0.2
    N_STEPS: int = 300

    # -----------------------------
    # 3D domain
    # -----------------------------
    DOMAIN_X: float = 40.0
    DOMAIN_Y: float = 40.0
    DOMAIN_Z: float = 40.0
    PERIODIC_BOUNDARIES: bool = True

    # -----------------------------
    # Initial population
    # -----------------------------
    INITIAL_MALES: int = 18
    INITIAL_FEMALES: int = 18
    INITIAL_HERMAPHRODITES: int = 12

    # -----------------------------
    # Movement
    # -----------------------------
    BASE_SPEED: float = 0.9
    MALE_TARGETING_STRENGTH: float = 2.2
    RANDOM_MOTION_STRENGTH: float = 0.8
    STRESS_RANDOM_BOOST: float = 0.4
    SENSING_RADIUS: float = 8.0
    MAX_SPEED: float = 2.2

    # -----------------------------
    # Interactions and reproduction
    # -----------------------------
    MATING_RADIUS: float = 1.4
    FEMALE_FERTILIZATION_PROB: float = 0.18
    HERMAPHRODITE_SELFING_PROB: float = 0.035

    FEMALE_OFFSPRING_MIN: int = 1
    FEMALE_OFFSPRING_MAX: int = 2
    HERMAPHRODITE_OFFSPRING_MIN: int = 1
    HERMAPHRODITE_OFFSPRING_MAX: int = 2

    OFFSPRING_PROB_MALE: float = 0.25
    OFFSPRING_PROB_FEMALE: float = 0.35
    OFFSPRING_PROB_HERMAPHRODITE: float = 0.40

    REPRODUCTION_COOLDOWN: float = 2.0

    # -----------------------------
    # Aging
    # -----------------------------
    JUVENILE_AGE_THRESHOLD: float = 3.0
    ADULT_AGE_THRESHOLD: float = 5.5

    # -----------------------------
    # Mortality
    # -----------------------------
    MALE_LIFESPAN: float = 20.0
    FEMALE_LIFESPAN: float = 22.0
    HERMAPHRODITE_LIFESPAN: float = 22.0

    JUVENILE_DEATH_PROB: float = 0.006
    ADULT_STRESS_DEATH_PROB_FACTOR: float = 0.012

    # -----------------------------
    # Stress
    # -----------------------------
    CROWDING_RADIUS: float = 3.0
    CROWDING_STRESS_FACTOR: float = 0.05
    STRESS_DECAY: float = 0.04
    MAX_STRESS: float = 1.0

    # -----------------------------
    # Output: plots
    # -----------------------------
    SAVE_PLOTS: bool = True
    SHOW_PLOTS: bool = False
    SAVE_DASHBOARD: bool = True

    PLOT_FILENAME_COUNTS: str = "population_counts.png"
    PLOT_FILENAME_EVENTS: str = "births_deaths.png"
    PLOT_FILENAME_STAGES: str = "life_stages.png"
    PLOT_FILENAME_FRACTIONS: str = "sex_fractions.png"
    PLOT_FILENAME_DASHBOARD: str = "population_dashboard.png"

    # -----------------------------
    # Output: animation
    # -----------------------------
    SAVE_ANIMATION: bool = True
    ANIMATION_FILENAME: str = "auanema_3d_animation.gif"
    ANIMATION_FPS: int = 10
    ANIMATION_EVERY_N_STEPS: int = 2

    TRAIL_LENGTH: int = 12
    MAX_TRAIL_AGENTS_PER_TYPE: int = 3

    # -----------------------------
    # Console output
    # -----------------------------
    VERBOSE: bool = True
    PRINT_EVERY: int = 20