"""
Main script to run Reynolds boids simulation.
"""
import numpy as np
from config.config_2d import Config2D
from config.config_3d import Config3D
from core.simulation import Simulation
from visualization.plot_2d import plot_2d_snapshot
from visualization.animate_2d import animate_2d
from visualization.plot_3d import plot_3d_snapshot, plot_3d_projections
from visualization.animate_3d import animate_3d
from analysis.diagnostics import run_diagnostics


def run_2d_simulation():
    """Run a 2D boids simulation."""
    print("\n" + "="*60)
    print("RUNNING 2D REYNOLDS BOIDS SIMULATION")
    print("="*60 + "\n")
    
    # Create configuration
    config = Config2D()
    
    # Create and run simulation
    sim = Simulation(config)
    history = sim.run()
    
    print("\nSimulation complete!")
    print(f"Saved {len(history)} snapshots")
    
    # Create visualizations
    print("\nCreating visualizations...")
    plot_2d_snapshot(history[-1], config, filename='boids_2d_final.png')
    animate_2d(history, config, filename='boids_2d.gif', fps=30)  # Changed to .gif
    
    # Run diagnostics
    run_diagnostics(history, config)
    
    return history, config


def run_3d_simulation():
    """Run a 3D boids simulation."""
    print("\n" + "="*60)
    print("RUNNING 3D REYNOLDS BOIDS SIMULATION")
    print("="*60 + "\n")
    
    # Create configuration
    config = Config3D()
    
    # Create and run simulation
    sim = Simulation(config)
    history = sim.run()
    
    print("\nSimulation complete!")
    print(f"Saved {len(history)} snapshots")
    
    # Create visualizations
    print("\nCreating visualizations...")
    plot_3d_snapshot(history[-1], config, filename='boids_3d_final.png')
    plot_3d_projections(history[-1], config, filename='boids_3d_projections.png')
    animate_3d(history, config, filename='boids_3d.gif', fps=30, rotate=True)  # Changed to .gif
    
    # Run diagnostics
    run_diagnostics(history, config)
    
    return history, config


if __name__ == '__main__':
    # Choose which simulation to run
    print("\nReynolds Boids Simulation")
    print("1. Run 2D simulation")
    print("2. Run 3D simulation")
    print("3. Run both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '1':
        run_2d_simulation()
    elif choice == '2':
        run_3d_simulation()
    elif choice == '3':
        run_2d_simulation()
        run_3d_simulation()
    else:
        print("Invalid choice. Running 2D simulation by default...")
        run_2d_simulation()
    
    print("\n" + "="*60)
    print("ALL SIMULATIONS COMPLETE")
    print("="*60 + "\n")