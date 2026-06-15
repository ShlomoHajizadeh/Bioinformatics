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
    DOMAIN_X: float = 32.0
    DOMAIN_Y: float = 32.0
    DOMAIN_Z: float = 32.0
    PERIODIC_BOUNDARIES: bool = True

    # voxel grid for nutrient / pheromone fields
    GRID_NX: int = 12
    GRID_NY: int = 12
    GRID_NZ: int = 12

    # -----------------------------
    # Initial population
    # -----------------------------
    INITIAL_MALES: int = 24
    INITIAL_FEMALES: int = 24
    INITIAL_HERMAPHRODITES: int = 16

    # -----------------------------
    # Movement
    # -----------------------------
    BASE_SPEED: float = 1.0
    MALE_TARGETING_STRENGTH: float = 2.4
    MALE_PHEROMONE_STRENGTH: float = 1.8
    RANDOM_MOTION_STRENGTH: float = 0.8
    STRESS_RANDOM_BOOST: float = 0.5
    SENSING_RADIUS: float = 10.0
    MAX_SPEED: float = 2.5

    # -----------------------------
    # Interactions and reproduction
    # -----------------------------
    MATING_RADIUS: float = 1.8
    FEMALE_FERTILIZATION_PROB: float = 0.28
    HERMAPHRODITE_SELFING_PROB: float = 0.07

    FEMALE_OFFSPRING_MIN: int = 1
    FEMALE_OFFSPRING_MAX: int = 3
    HERMAPHRODITE_OFFSPRING_MIN: int = 1
    HERMAPHRODITE_OFFSPRING_MAX: int = 2

    OFFSPRING_PROB_MALE: float = 0.25
    OFFSPRING_PROB_FEMALE: float = 0.35
    OFFSPRING_PROB_HERMAPHRODITE: float = 0.40

    REPRODUCTION_COOLDOWN: float = 1.4

    # -----------------------------
    # Aging
    # -----------------------------
    JUVENILE_AGE_THRESHOLD: float = 3.0
    ADULT_AGE_THRESHOLD: float = 5.5

    # -----------------------------
    # Mortality
    # -----------------------------
    MALE_LIFESPAN: float = 24.0
    FEMALE_LIFESPAN: float = 26.0
    HERMAPHRODITE_LIFESPAN: float = 26.0

    JUVENILE_DEATH_PROB: float = 0.003
    ADULT_STRESS_DEATH_PROB_FACTOR: float = 0.006

    # -----------------------------
    # Stress
    # -----------------------------
    CROWDING_RADIUS: float = 3.0
    CROWDING_STRESS_FACTOR: float = 0.025
    STRESS_DECAY: float = 0.04
    MAX_STRESS: float = 1.0

    # nutrient/stress coupling
    LOW_NUTRIENT_THRESHOLD: float = 0.20
    LOW_NUTRIENT_STRESS_INCREASE: float = 0.04
    NUTRIENT_REPRODUCTION_CUTOFF: float = 0.10

    # -----------------------------
    # Environment fields
    # -----------------------------
    INITIAL_NUTRIENT_LEVEL: float = 1.0
    NUTRIENT_REGEN_RATE: float = 0.015
    NUTRIENT_MAX: float = 1.0

    NUTRIENT_CONSUMPTION_JUVENILE: float = 0.015
    NUTRIENT_CONSUMPTION_ADULT: float = 0.025
    NUTRIENT_CONSUMPTION_REPRODUCTIVE: float = 0.035

    FEMALE_PHEROMONE_DEPOSIT: float = 0.10
    HERMAPHRODITE_PHEROMONE_DEPOSIT: float = 0.08
    PHEROMONE_DECAY_RATE: float = 0.015
    PHEROMONE_DIFFUSION_STRENGTH: float = 0.12
    PHEROMONE_MAX: float = 6.0

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
    PLOT_FILENAME_STRESS: str = "stress_and_environment.png"

    # -----------------------------
    # Output: animation
    # -----------------------------
    SAVE_ANIMATION: bool = True
    ANIMATION_FILENAME: str = "auanema_3d_animation.gif"
    ANIMATION_FPS: int = 8
    ANIMATION_EVERY_N_STEPS: int = 4

    TRAIL_LENGTH: int = 10
    MAX_TRAIL_AGENTS_PER_TYPE: int = 3

    NUTRIENT_DISPLAY_THRESHOLD: float = 0.05
    PHEROMONE_DISPLAY_THRESHOLD: float = 0.02

    # -----------------------------
    # Console output
    # -----------------------------
    VERBOSE: bool = True
    PRINT_EVERY: int = 20