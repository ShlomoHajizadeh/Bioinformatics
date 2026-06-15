from pathlib import Path

PROJECT_NAME = "auanema_3d_simulation"

DIRECTORIES = [
    PROJECT_NAME,
    f"{PROJECT_NAME}/config",
    f"{PROJECT_NAME}/core",
    f"{PROJECT_NAME}/output",
    f"{PROJECT_NAME}/tests",
]

FILES = [
    f"{PROJECT_NAME}/README.md",
    f"{PROJECT_NAME}/requirements.txt",

    f"{PROJECT_NAME}/config/__init__.py",
    f"{PROJECT_NAME}/config/config.py",

    f"{PROJECT_NAME}/core/__init__.py",
    f"{PROJECT_NAME}/core/enums.py",
    f"{PROJECT_NAME}/core/agent.py",
    f"{PROJECT_NAME}/core/population.py",
    f"{PROJECT_NAME}/core/environment.py",
    f"{PROJECT_NAME}/core/movement.py",
    f"{PROJECT_NAME}/core/interactions.py",
    f"{PROJECT_NAME}/core/reproduction.py",
    f"{PROJECT_NAME}/core/aging.py",
    f"{PROJECT_NAME}/core/mortality.py",
    f"{PROJECT_NAME}/core/simulation.py",
    f"{PROJECT_NAME}/core/utils.py",

    f"{PROJECT_NAME}/output/__init__.py",
    f"{PROJECT_NAME}/output/statistics.py",
    f"{PROJECT_NAME}/output/plots.py",
    f"{PROJECT_NAME}/output/animation.py",

    f"{PROJECT_NAME}/tests/__init__.py",
    f"{PROJECT_NAME}/tests/test_agent.py",
    f"{PROJECT_NAME}/tests/test_movement.py",
    f"{PROJECT_NAME}/tests/test_interactions.py",
    f"{PROJECT_NAME}/tests/test_reproduction.py",
    f"{PROJECT_NAME}/tests/test_aging.py",
    f"{PROJECT_NAME}/tests/test_simulation.py",

    f"{PROJECT_NAME}/main.py",
]


def create_project_structure() -> None:
    """
    Create the folder structure and empty files for the project.
    Existing folders/files are left untouched.
    """
    for directory in DIRECTORIES:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Directory ready: {path}")

    for file_path in FILES:
        path = Path(file_path)
        path.touch(exist_ok=True)
        print(f"File ready:      {path}")

    print("\nProject structure created successfully.")


if __name__ == "__main__":
    create_project_structure()