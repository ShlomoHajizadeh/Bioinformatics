from pathlib import Path

PROJECT_NAME = "tobacco_tritrophic_model"

FOLDERS = [
    PROJECT_NAME,
    f"{PROJECT_NAME}/config",
    f"{PROJECT_NAME}/core",
    f"{PROJECT_NAME}/output",
    f"{PROJECT_NAME}/tests",
]

FILES = [
    f"{PROJECT_NAME}/README.md",
    f"{PROJECT_NAME}/requirements.txt",
    f"{PROJECT_NAME}/main.py",
    f"{PROJECT_NAME}/config/config.py",
    f"{PROJECT_NAME}/core/__init__.py",
    f"{PROJECT_NAME}/core/grid.py",
    f"{PROJECT_NAME}/core/clock.py",
    f"{PROJECT_NAME}/core/plant_dynamics.py",
    f"{PROJECT_NAME}/core/signaling.py",
    f"{PROJECT_NAME}/core/moth_dynamics.py",
    f"{PROJECT_NAME}/core/caterpillar_dynamics.py",
    f"{PROJECT_NAME}/core/predator_dynamics.py",
    f"{PROJECT_NAME}/core/interactions.py",
    f"{PROJECT_NAME}/core/simulation.py",
    f"{PROJECT_NAME}/output/__init__.py",
    f"{PROJECT_NAME}/output/plots.py",
    f"{PROJECT_NAME}/output/animation.py",
    f"{PROJECT_NAME}/output/snapshots.py",
    f"{PROJECT_NAME}/tests/__init__.py",
    f"{PROJECT_NAME}/tests/test_clock.py",
    f"{PROJECT_NAME}/tests/test_plant_dynamics.py",
    f"{PROJECT_NAME}/tests/test_signaling.py",
    f"{PROJECT_NAME}/tests/test_moth_dynamics.py",
    f"{PROJECT_NAME}/tests/test_predator_dynamics.py",
    f"{PROJECT_NAME}/tests/test_simulation.py",
]


def create_project_structure():
    # Create folders
    for folder in FOLDERS:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {folder}")

    # Create empty files
    for file in FILES:
        path = Path(file)
        path.touch(exist_ok=True)
        print(f"Created file:   {file}")


if __name__ == "__main__":
    create_project_structure()
    print("\nProject structure created successfully.")