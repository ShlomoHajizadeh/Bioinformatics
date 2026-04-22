from pathlib import Path

# ------------------------------------------------------------
# Chase-and-escape project structure generator
# ------------------------------------------------------------

PROJECT_NAME = "chase_escape_simulation"

STRUCTURE = {
    "": [
        "README.md",
        "requirements.txt",
        "main.py",
    ],
    "config": [
        "__init__.py",
        "config.py",
    ],
    "core": [
        "__init__.py",
        "lattice.py",
        "agents.py",
        "distance.py",
        "movement.py",
        "capture.py",
        "simulation.py",
        "utils.py",
    ],
    "visualization": [
        "__init__.py",
        "plotters.py",
        "animation.py",
        "snapshots.py",
    ],
    "analysis": [
        "__init__.py",
        "observables.py",
        "reporter.py",
    ],
    "tests": [
        "__init__.py",
        "test_distance.py",
        "test_movement_targets.py",
        "test_movement_chasers.py",
        "test_capture.py",
        "test_simulation.py",
    ],
    "prompts": [
        "prompt_01_lattice.md",
        "prompt_02_distance.md",
        "prompt_03_agents.md",
        "prompt_04_target_motion.md",
        "prompt_05_chaser_motion.md",
        "prompt_06_capture.md",
        "prompt_07_simulation_loop.md",
        "prompt_08_visualization.md",
        "prompt_09_tests.md",
    ],
}


def create_project_structure(base_path: Path, project_name: str, structure: dict) -> None:
    """
    Create the project folder structure and empty files.

    Parameters
    ----------
    base_path : Path
        Directory in which the project folder should be created.
    project_name : str
        Name of the top-level project folder.
    structure : dict
        Dictionary mapping folder names to lists of files.
    """
    project_root = base_path / project_name
    project_root.mkdir(parents=True, exist_ok=True)

    for folder, files in structure.items():
        folder_path = project_root / folder if folder else project_root
        folder_path.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            file_path = folder_path / file_name
            file_path.touch(exist_ok=True)

    print(f"Project structure created successfully at:\n{project_root.resolve()}")


if __name__ == "__main__":
    # Change this path if you want the project somewhere else.
    # Example for Windows:
    # base_directory = Path(r"C:\Users\YourName\Documents")
    base_directory = Path.cwd()

    create_project_structure(base_directory, PROJECT_NAME, STRUCTURE)