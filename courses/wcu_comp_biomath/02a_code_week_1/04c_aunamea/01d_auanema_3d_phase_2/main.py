from config.config import SimulationConfig
from core.simulation import run_simulation
from output.plots import create_all_plots, create_dashboard_plot
from output.animation import create_3d_animation_with_fields


def main():
    config = SimulationConfig()

    (
        population,
        environment,
        stats,
        history_snapshots,
        nutrient_history,
        pheromone_history,
    ) = run_simulation(config)

    if config.SAVE_PLOTS:
        create_all_plots(stats, config)
        print("Saved plots:")
        print(f"  {config.PLOT_FILENAME_COUNTS}")
        print(f"  {config.PLOT_FILENAME_EVENTS}")
        print(f"  {config.PLOT_FILENAME_STAGES}")
        print(f"  {config.PLOT_FILENAME_FRACTIONS}")
        print(f"  {config.PLOT_FILENAME_STRESS}")

    if config.SAVE_DASHBOARD:
        create_dashboard_plot(stats, config)
        print(f"Saved dashboard: {config.PLOT_FILENAME_DASHBOARD}")

    if config.SAVE_ANIMATION and len(history_snapshots) > 0:
        create_3d_animation_with_fields(
            history_snapshots=history_snapshots,
            nutrient_history=nutrient_history,
            pheromone_history=pheromone_history,
            environment=environment,
            filename=config.ANIMATION_FILENAME,
            fps=config.ANIMATION_FPS,
            trail_length=config.TRAIL_LENGTH,
            max_trail_agents_per_type=config.MAX_TRAIL_AGENTS_PER_TYPE,
            nutrient_threshold=config.NUTRIENT_DISPLAY_THRESHOLD,
            pheromone_threshold=config.PHEROMONE_DISPLAY_THRESHOLD,
        )
        print(f"Saved animation: {config.ANIMATION_FILENAME}")

    print("\nFinal population:")
    print(f"  total          = {population.count_total()}")
    print(f"  males          = {stats.males[-1] if stats.males else 0}")
    print(f"  females        = {stats.females[-1] if stats.females else 0}")
    print(f"  hermaphrodites = {stats.hermaphrodites[-1] if stats.hermaphrodites else 0}")
    print(f"  mean nutrient  = {stats.mean_nutrient[-1] if stats.mean_nutrient else 0.0:.3f}")
    print(f"  mean pheromone = {stats.mean_pheromone[-1] if stats.mean_pheromone else 0.0:.3f}")
    print(f"  mean stress    = {stats.mean_stress[-1] if stats.mean_stress else 0.0:.3f}")


if __name__ == "__main__":
    main()