import os

# Root project name
PROJECT_NAME = "invasive_species_model"

# Folder + file structure
STRUCTURE = {
    "": ["README.md", "requirements.txt", "main.py"],

    "config": ["config.py"],

    "environment": ["__init__.py", "habitat.py", "lattice.py"],

    "agents": [
        "__init__.py",
        "base_agent.py",
        "native_trout.py",
        "invasive_trout.py",
        "bear.py",
        "bird.py",
        "elk.py",
    ],

    "core": [
        "__init__.py",
        "initializer.py",
        "movement.py",
        "interactions.py",
        "reproduction.py",
        "mortality.py",
        "carrying_capacity.py",
        "scheduler.py",
        "simulation.py",
    ],

    "output": [
        "__init__.py",
        "metrics.py",
        "visualizer.py",
        "animation.py",
        "reporter.py",
    ],

    "utils": [
        "__init__.py",
        "rng_utils.py",
        "torus.py",
        "validation.py",
    ],

    "tests": [
        "__init__.py",
        "test_habitat.py",
        "test_movement.py",
        "test_interactions.py",
        "test_reproduction.py",
        "test_mortality.py",
        "test_simulation_smoke.py",
    ],
}


def create_structure(base_path):
    for folder, files in STRUCTURE.items():
        folder_path = os.path.join(base_path, folder)

        # Create folder (including root if "")
        os.makedirs(folder_path, exist_ok=True)

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)

            # Create empty file if it does not exist
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")  # empty file

                print(f"Created file: {file_path}")
            else:
                print(f"File already exists: {file_path}")


if __name__ == "__main__":
    base_path = os.path.join(os.getcwd(), PROJECT_NAME)

    os.makedirs(base_path, exist_ok=True)
    print(f"Creating project at: {base_path}")

    create_structure(base_path)

    print("\nProject structure created successfully.")
