"""Main simulation script for the Vicsek flocking model."""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from config import VicsekConfig
from state import initialize_state
from dynamics import step
from diagnostics import order_parameter, summary_statistics
from visualization import plot_state


def run_simulation(config: VicsekConfig, verbose: bool = True):
    """Run a complete Vicsek model simulation.
    
    Args:
        config: Vicsek configuration parameters
        verbose: Whether to print progress information
        
    Returns:
        trajectory: Dictionary containing simulation results
    """
    # Set random seed for reproducibility
    if config.seed is not None:
        np.random.seed(config.seed)
    
    # Initialize state
    positions, headings = initialize_state(config)
    
    # Storage for trajectory data
    trajectory = {
        'positions': [positions.copy()],
        'headings': [headings.copy()],
        'order_parameter': [order_parameter(headings)],
        'time': [0]
    }
    
    # Run simulation
    for n in range(config.n_steps):
        # Perform one time step
        positions, headings = step(positions, headings, config)
        
        # Store results
        trajectory['positions'].append(positions.copy())
        trajectory['headings'].append(headings.copy())
        trajectory['order_parameter'].append(order_parameter(headings))
        trajectory['time'].append((n + 1) * config.h)
        
        # Print progress
        if verbose and (n + 1) % 100 == 0:
            order = trajectory['order_parameter'][-1]
            print(f"Step {n + 1}/{config.n_steps}, Order parameter: {order:.4f}")
    
    return trajectory


def plot_trajectory_summary(trajectory: dict, config: VicsekConfig, 
                           save_path: str = None):
    """Create summary plots of the simulation trajectory.
    
    Args:
        trajectory: Dictionary with simulation results
        config: Vicsek configuration parameters
        save_path: Optional path to save the figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Initial state
    ax1 = axes[0, 0]
    plot_state(trajectory['positions'][0], trajectory['headings'][0], 
               config, ax=ax1)
    ax1.set_title('Initial State (t=0)')
    
    # Plot 2: Final state
    ax2 = axes[0, 1]
    plot_state(trajectory['positions'][-1], trajectory['headings'][-1], 
               config, ax=ax2)
    ax2.set_title(f'Final State (t={trajectory["time"][-1]:.1f})')
    
    # Plot 3: Order parameter evolution
    ax3 = axes[1, 0]
    ax3.plot(trajectory['time'], trajectory['order_parameter'], 
             linewidth=2, color='darkblue')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Order Parameter')
    ax3.set_title('Order Parameter Evolution')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Heading distribution (final state)
    ax4 = axes[1, 1]
    ax4.hist(trajectory['headings'][-1], bins=30, density=True, 
             alpha=0.7, color='green', edgecolor='black')
    ax4.set_xlabel('Heading Angle (rad)')
    ax4.set_ylabel('Probability Density')
    ax4.set_title('Final Heading Distribution')
    ax4.set_xlim(-np.pi, np.pi)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {save_path}")
    
    plt.show()


def main():
    """Main entry point for Vicsek model simulation."""
    
    # Create configuration with specific parameters
    config = VicsekConfig(
        N=300,           # Number of particles
        L=10.0,          # Domain size
        r=1.0,           # Interaction radius
        nu_0=0.5,        # Absolute velocity
        eta=0.5,         # Noise strength
        h=1.0,           # Time step
        n_steps=500,     # Number of simulation steps
        seed=42          # Random seed for reproducibility
    )
    
    print("="*60)
    print("Vicsek Flocking Model Simulation")
    print("="*60)
    print(f"Parameters:")
    print(f"  N (particles):        {config.N}")
    print(f"  L (domain size):      {config.L}")
    print(f"  r (interaction):      {config.r}")
    print(f"  ν₀ (velocity):        {config.nu_0}")
    print(f"  η (noise):            {config.eta}")
    print(f"  h (time step):        {config.h}")
    print(f"  n_steps:              {config.n_steps}")
    print(f"  seed:                 {config.seed}")
    print("="*60)
    print()
    
    # Run simulation
    print("Running simulation...")
    trajectory = run_simulation(config, verbose=True)
    print()
    
    # Print final statistics
    final_positions = trajectory['positions'][-1]
    final_headings = trajectory['headings'][-1]
    stats = summary_statistics(final_positions, final_headings, config)
    
    print("="*60)
    print("Final Statistics:")
    print("="*60)
    print(f"  Order parameter:      {stats['order_parameter']:.4f}")
    print(f"  Mean heading:         {stats['mean_heading']:.4f} rad")
    print(f"  Heading std:          {stats['heading_std']:.4f} rad")
    print(f"  Center of mass:       ({stats['center_of_mass'][0]:.2f}, "
          f"{stats['center_of_mass'][1]:.2f})")
    print("="*60)
    print()
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Plot results
    print("Generating plots...")
    plot_trajectory_summary(trajectory, config, 
                          save_path=output_dir / "vicsek_summary.png")
    
    print("\nSimulation complete!")
    
    return trajectory, config


if __name__ == "__main__":
    trajectory, config = main()