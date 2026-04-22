from config.config import Config
from core.simulation import Simulation
from visualization.plotters import plot_lattice, plot_targets
from visualization.snapshots import save_lattice_snapshot
from visualization.animation import animate_simulation, save_animation_gif


def main():
    cfg = Config()
    sim = Simulation(cfg)

    sim.run()

    # Save final snapshot as PNG
    save_lattice_snapshot(
        sim.grid,
        filename="final_snapshot.png",
        title="Final lattice state",
    )

    # Create animation object from stored lattice history
    anim = animate_simulation(
        sim.history_grids,
        interval=200,
        title="Chase-and-Escape Animation",
        show=True,
    )

    # Save animation as GIF
    save_animation_gif(
        anim,
        filename="chase_escape_animation.gif",
        fps=5,
    )

    # Plot final lattice state
    plot_lattice(sim.grid)

    # Plot time series of surviving targets
    plot_targets(sim.history_targets)

    return anim


if __name__ == "__main__":
    animation = main()