"""
Create complete folder and file structure for Reynolds Boids project.
"""

import os


def create_structure():
    """Create the complete folder and file structure."""
    
    base_dir = "reynolds_boids"
    
    # Define all files to create
    files = [
        # Root level
        f"{base_dir}/README.md",
        f"{base_dir}/requirements.txt",
        f"{base_dir}/main.py",
        
        # Config
        f"{base_dir}/config/config_2d.py",
        f"{base_dir}/config/config_3d.py",
        
        # Core
        f"{base_dir}/core/__init__.py",
        f"{base_dir}/core/state.py",
        f"{base_dir}/core/domain.py",
        f"{base_dir}/core/initialization.py",
        f"{base_dir}/core/neighbors.py",
        f"{base_dir}/core/rules.py",
        f"{base_dir}/core/integrator.py",
        f"{base_dir}/core/simulation.py",
        
        # Visualization
        f"{base_dir}/visualization/__init__.py",
        f"{base_dir}/visualization/plot_2d.py",
        f"{base_dir}/visualization/animate_2d.py",
        f"{base_dir}/visualization/plot_3d.py",
        f"{base_dir}/visualization/animate_3d.py",
        
        # Analysis
        f"{base_dir}/analysis/__init__.py",
        f"{base_dir}/analysis/metrics.py",
        f"{base_dir}/analysis/diagnostics.py",
        
        # Tests
        f"{base_dir}/tests/test_domain.py",
        f"{base_dir}/tests/test_neighbors.py",
        f"{base_dir}/tests/test_rules.py",
        f"{base_dir}/tests/test_simulation.py"
    ]
    
    print("Creating folder and file structure...\n")
    
    for filepath in files:
        # Create directory if it doesn't exist
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        # Create empty file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("")
        
        print(f"Created: {filepath}")
    
    print("\n" + "="*60)
    print("Folder and file structure created successfully!")
    print("="*60)
    print(f"\nProject location: ./{base_dir}/")
    print("\nAll files are currently empty.")
    print("You can now copy the content into each file.")


if __name__ == '__main__':
    create_structure()