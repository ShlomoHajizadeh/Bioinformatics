"""
setup_project.py

Creates the full folder structure for the
'prisoner_dilemma_evolution' project,
including empty Python files with minimal content.
"""

import os


# -----------------------------
# Project structure definition
# -----------------------------
PROJECT_NAME = "prisoner_dilemma_evolution"

STRUCTURE = {
    "": ["README.md", "requirements.txt", "main.py"],
    "config": ["config.py"],
    "core": ["__init__.py", "game.py", "tournament.py", "evolution.py"],
    "strategies": [
        "__init__.py",
        "base_strategy.py",
        "always_cooperate.py",
        "always_defect.py",
        "tit_for_tat.py",
        "random_strategy.py",
        "grudger.py",
    ],
    "output": ["__init__.py", "visualizer.py", "reporter.py"],
    "tests": [
        "__init__.py",
        "test_game.py",
        "test_tournament.py",
        "test_evolution.py",
        "test_strategies.py",
    ],
}


# -----------------------------
# Default file contents
# -----------------------------
def default_content(file_name):
    if file_name == "__init__.py":
        return ""

    if file_name.endswith(".py"):
        return f'"""{file_name}"""\n\n'

    if file_name == "README.md":
        return "# Prisoner's Dilemma Evolution Project\n\n"

    if file_name == "requirements.txt":
        return "# Add dependencies here\n"

    return ""


# -----------------------------
# Create structure
# -----------------------------
def create_project():
    print(f"Creating project: {PROJECT_NAME}\n")

    for folder, files in STRUCTURE.items():
        folder_path = os.path.join(PROJECT_NAME, folder)

        # Create directory
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(folder_path, file)

            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write(default_content(file))

                print(f"Created: {file_path}")
            else:
                print(f"Exists:  {file_path}")

    print("\nProject structure created successfully.")


# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    create_project()