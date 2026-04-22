"""
Setup script for Yellowstone Wolf-Bison-Ecosystem Model
Creates the complete folder structure and empty files for the project.
"""

import os


def create_project_structure():
    """
    Creates all folders and files for the Yellowstone simulation project.
    """
    
    # Define the project structure
    structure = {
        'Yellowstone': {
            'files': ['main.py', 'README.md', 'requirements.txt'],
            'subdirs': {
                'config': {
                    'files': ['__init__.py', 'config.py', 'initialization.py'],
                    'subdirs': {}
                },
                'model': {
                    'files': [
                        '__init__.py',
                        'grid.py',
                        'environment.py',
                        'agents.py',
                        'movement.py',
                        'interactions.py',
                        'update_rules.py',
                        'simulation.py'
                    ],
                    'subdirs': {}
                },
                'visualization': {
                    'files': ['__init__.py', 'plot.py', 'animation.py'],
                    'subdirs': {}
                },
                'analysis': {
                    'files': ['__init__.py', 'metrics.py'],
                    'subdirs': {}
                },
                'tests': {
                    'files': ['__init__.py'],
                    'subdirs': {}
                }
            }
        }
    }
    
    def create_structure(base_path, structure_dict):
        """
        Recursively creates folders and files based on structure dictionary.
        
        Args:
            base_path: Current directory path
            structure_dict: Dictionary defining structure
        """
        # Create the base directory if it doesn't exist
        os.makedirs(base_path, exist_ok=True)
        print(f"Created directory: {base_path}")
        
        # Create files in current directory
        if 'files' in structure_dict:
            for filename in structure_dict['files']:
                filepath = os.path.join(base_path, filename)
                with open(filepath, 'w') as f:
                    pass  # Create empty file
                print(f"  Created file: {filepath}")
        
        # Recursively create subdirectories
        if 'subdirs' in structure_dict:
            for subdir_name, subdir_content in structure_dict['subdirs'].items():
                subdir_path = os.path.join(base_path, subdir_name)
                create_structure(subdir_path, subdir_content)
    
    # Create the entire structure
    for root_dir, content in structure.items():
        create_structure(root_dir, content)
    
    print("\n" + "="*60)
    print("Project structure created successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Navigate to the Yellowstone directory")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Start implementing the model files")
    print("\nFolder structure:")
    print("""
Yellowstone/
├── main.py
├── README.md
├── requirements.txt
├── config/
│   ├── __init__.py
│   ├── config.py
│   └── initialization.py
├── model/
│   ├── __init__.py
│   ├── grid.py
│   ├── environment.py
│   ├── agents.py
│   ├── movement.py
│   ├── interactions.py
│   ├── update_rules.py
│   └── simulation.py
├── visualization/
│   ├── __init__.py
│   ├── plot.py
│   └── animation.py
├── analysis/
│   ├── __init__.py
│   └── metrics.py
└── tests/
    └── __init__.py
    """)


if __name__ == "__main__":
    create_project_structure()