import matplotlib.pyplot as plt
import numpy as np


def _finalize_plot(config, filename):
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    if config.SHOW_PLOTS:
        plt.show()
    plt.close()


def plot_population_counts(stats, config):
    plt.figure(figsize=(10, 6))
    plt.plot(stats.time, stats.total_population, label="total population", linewidth=2)
    plt.plot(stats.time, stats.males, label="males")
    plt.plot(stats.time, stats.females, label="females")
    plt.plot(stats.time, stats.hermaphrodites, label="hermaphrodites")
    plt.xlabel("time")
    plt.ylabel("count")
    plt.title("Population counts over time")
    plt.legend()
    plt.grid(True)
    _finalize_plot(config, config.PLOT_FILENAME_COUNTS)


def plot_births_deaths(stats, config):
    plt.figure(figsize=(10, 6))
    plt.plot(stats.time, stats.births, label="births per step")
    plt.plot(stats.time, stats.deaths, label="deaths per step")
    plt.xlabel("time")
    plt.ylabel("count")
    plt.title("Births and deaths over time")
    plt.legend()
    plt.grid(True)
    _finalize_plot(config, config.PLOT_FILENAME_EVENTS)


def plot_life_stages(stats, config):
    plt.figure(figsize=(10, 6))
    plt.plot(stats.time, stats.juveniles, label="juveniles")
    plt.plot(stats.time, stats.adults, label="adults")
    plt.plot(stats.time, stats.reproductive_adults, label="reproductive adults")
    plt.xlabel("time")
    plt.ylabel("count")
    plt.title("Life stages over time")
    plt.legend()
    plt.grid(True)
    _finalize_plot(config, config.PLOT_FILENAME_STAGES)


def plot_sex_fractions(stats, config):
    total = np.array(stats.total_population, dtype=float)
    total[total == 0.0] = 1.0

    male_frac = np.array(stats.males, dtype=float) / total
    female_frac = np.array(stats.females, dtype=float) / total
    herm_frac = np.array(stats.hermaphrodites, dtype=float) / total

    plt.figure(figsize=(10, 6))
    plt.plot(stats.time, male_frac, label="male fraction")
    plt.plot(stats.time, female_frac, label="female fraction")
    plt.plot(stats.time, herm_frac, label="hermaphrodite fraction")
    plt.xlabel("time")
    plt.ylabel("fraction")
    plt.title("Population sex fractions over time")
    plt.ylim(0.0, 1.0)
    plt.legend()
    plt.grid(True)
    _finalize_plot(config, config.PLOT_FILENAME_FRACTIONS)


def plot_stress_and_environment(stats, config):
    plt.figure(figsize=(10, 6))
    plt.plot(stats.time, stats.mean_stress, label="mean stress")
    plt.plot(stats.time, stats.mean_nutrient, label="mean nutrient")
    plt.plot(stats.time, stats.mean_pheromone, label="mean pheromone")
    plt.xlabel("time")
    plt.ylabel("mean value")
    plt.title("Stress and environment over time")
    plt.legend()
    plt.grid(True)
    _finalize_plot(config, config.PLOT_FILENAME_STRESS)


def create_all_plots(stats, config):
    plot_population_counts(stats, config)
    plot_births_deaths(stats, config)
    plot_life_stages(stats, config)
    plot_sex_fractions(stats, config)
    plot_stress_and_environment(stats, config)


def create_dashboard_plot(stats, config):
    total = np.array(stats.total_population, dtype=float)
    total_safe = total.copy()
    total_safe[total_safe == 0.0] = 1.0

    male_frac = np.array(stats.males, dtype=float) / total_safe
    female_frac = np.array(stats.females, dtype=float) / total_safe
    herm_frac = np.array(stats.hermaphrodites, dtype=float) / total_safe

    fig = plt.figure(figsize=(14, 10))

    ax1 = fig.add_subplot(2, 3, 1)
    ax1.plot(stats.time, stats.total_population, label="total", linewidth=2)
    ax1.plot(stats.time, stats.males, label="males")
    ax1.plot(stats.time, stats.females, label="females")
    ax1.plot(stats.time, stats.hermaphrodites, label="hermaphrodites")
    ax1.set_title("Population counts")
    ax1.set_xlabel("time")
    ax1.set_ylabel("count")
    ax1.grid(True)
    ax1.legend()

    ax2 = fig.add_subplot(2, 3, 2)
    ax2.plot(stats.time, stats.births, label="births")
    ax2.plot(stats.time, stats.deaths, label="deaths")
    ax2.set_title("Births and deaths")
    ax2.set_xlabel("time")
    ax2.set_ylabel("count")
    ax2.grid(True)
    ax2.legend()

    ax3 = fig.add_subplot(2, 3, 3)
    ax3.plot(stats.time, stats.juveniles, label="juveniles")
    ax3.plot(stats.time, stats.adults, label="adults")
    ax3.plot(stats.time, stats.reproductive_adults, label="reproductive adults")
    ax3.set_title("Life stages")
    ax3.set_xlabel("time")
    ax3.set_ylabel("count")
    ax3.grid(True)
    ax3.legend()

    ax4 = fig.add_subplot(2, 3, 4)
    ax4.plot(stats.time, male_frac, label="male fraction")
    ax4.plot(stats.time, female_frac, label="female fraction")
    ax4.plot(stats.time, herm_frac, label="hermaphrodite fraction")
    ax4.set_title("Sex fractions")
    ax4.set_xlabel("time")
    ax4.set_ylabel("fraction")
    ax4.set_ylim(0.0, 1.0)
    ax4.grid(True)
    ax4.legend()

    ax5 = fig.add_subplot(2, 3, 5)
    ax5.plot(stats.time, stats.mean_stress, label="mean stress")
    ax5.plot(stats.time, stats.mean_nutrient, label="mean nutrient")
    ax5.set_title("Stress and nutrient")
    ax5.set_xlabel("time")
    ax5.set_ylabel("mean value")
    ax5.grid(True)
    ax5.legend()

    ax6 = fig.add_subplot(2, 3, 6)
    ax6.plot(stats.time, stats.mean_pheromone, label="mean pheromone")
    ax6.set_title("Pheromone level")
    ax6.set_xlabel("time")
    ax6.set_ylabel("mean value")
    ax6.grid(True)
    ax6.legend()

    plt.tight_layout()
    plt.savefig(config.PLOT_FILENAME_DASHBOARD, dpi=150)
    if config.SHOW_PLOTS:
        plt.show()
    plt.close(fig)