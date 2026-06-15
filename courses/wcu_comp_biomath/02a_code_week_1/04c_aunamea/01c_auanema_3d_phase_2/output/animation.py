import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from core.enums import SexType


def _extract_positions_by_type(snapshot_agents):
    male_positions = []
    female_positions = []
    herm_positions = []

    for agent in snapshot_agents:
        if not agent.alive:
            continue

        if agent.sex_type == SexType.MALE:
            male_positions.append(agent.position.copy())
        elif agent.sex_type == SexType.FEMALE:
            female_positions.append(agent.position.copy())
        else:
            herm_positions.append(agent.position.copy())

    def as_array(lst):
        if len(lst) == 0:
            return np.empty((0, 3), dtype=float)
        return np.array(lst, dtype=float)

    return as_array(male_positions), as_array(female_positions), as_array(herm_positions)


def _count_types(snapshot_agents):
    n_m = 0
    n_f = 0
    n_h = 0

    for agent in snapshot_agents:
        if not agent.alive:
            continue
        if agent.sex_type == SexType.MALE:
            n_m += 1
        elif agent.sex_type == SexType.FEMALE:
            n_f += 1
        else:
            n_h += 1

    return n_m, n_f, n_h


def _build_agent_history(history_snapshots):
    all_ids = set()
    for snapshot in history_snapshots:
        for agent in snapshot:
            if agent.alive:
                all_ids.add(agent.agent_id)

    agent_history = {agent_id: [] for agent_id in all_ids}

    for snapshot in history_snapshots:
        pos_map = {}
        for agent in snapshot:
            if agent.alive:
                pos_map[agent.agent_id] = agent.position.copy()

        for agent_id in all_ids:
            agent_history[agent_id].append(pos_map.get(agent_id, None))

    return agent_history


def _choose_trail_agents(history_snapshots, max_per_type=3):
    if len(history_snapshots) == 0:
        return []

    first_snapshot = history_snapshots[0]

    male_ids = []
    female_ids = []
    herm_ids = []

    for agent in first_snapshot:
        if not agent.alive:
            continue
        if agent.sex_type == SexType.MALE and len(male_ids) < max_per_type:
            male_ids.append(agent.agent_id)
        elif agent.sex_type == SexType.FEMALE and len(female_ids) < max_per_type:
            female_ids.append(agent.agent_id)
        elif agent.sex_type == SexType.HERMAPHRODITE and len(herm_ids) < max_per_type:
            herm_ids.append(agent.agent_id)

    return male_ids + female_ids + herm_ids


def _draw_trails(ax, frame, tracked_ids, agent_history, trail_length=12):
    for agent_id in tracked_ids:
        start = max(0, frame - trail_length + 1)
        segment = agent_history[agent_id][start:frame + 1]

        pts = [p for p in segment if p is not None]
        if len(pts) < 2:
            continue

        pts = np.array(pts, dtype=float)
        ax.plot(
            pts[:, 0],
            pts[:, 1],
            pts[:, 2],
            linewidth=1.2,
            alpha=0.7,
        )


def _grid_cell_centers(environment):
    xs = (np.arange(environment.grid_nx) + 0.5) * environment.dx
    ys = (np.arange(environment.grid_ny) + 0.5) * environment.dy
    zs = (np.arange(environment.grid_nz) + 0.5) * environment.dz

    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    return X, Y, Z


def _plot_field_3d(
    ax,
    field,
    environment,
    title,
    threshold=0.05,
    size_scale=80.0,
    cmap="viridis",
    marker="s",
):
    X, Y, Z = _grid_cell_centers(environment)

    mask = field > threshold

    if np.any(mask):
        values = field[mask]
        vmax = max(float(values.max()), 1e-12)
        sizes = 8.0 + size_scale * values / vmax

        ax.scatter(
            X[mask],
            Y[mask],
            Z[mask],
            c=values,
            s=sizes,
            cmap=cmap,
            alpha=0.35,
            marker=marker,
            edgecolors="none",
            depthshade=False,
            vmin=0.0,
            vmax=vmax,
        )

    ax.set_xlim(0, environment.x_size)
    ax.set_ylim(0, environment.y_size)
    ax.set_zlim(0, environment.z_size)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(title)


def create_3d_animation_with_fields(
    history_snapshots,
    nutrient_history,
    pheromone_history,
    environment,
    filename="auanema_3d_animation.gif",
    fps=10,
    trail_length=12,
    max_trail_agents_per_type=3,
    nutrient_threshold=0.05,
    pheromone_threshold=0.02,
):
    if len(history_snapshots) == 0:
        print("No animation snapshots available.")
        return

    agent_history = _build_agent_history(history_snapshots)
    tracked_ids = _choose_trail_agents(
        history_snapshots,
        max_per_type=max_trail_agents_per_type,
    )

    fig = plt.figure(figsize=(18, 6))

    ax_agents = fig.add_subplot(131, projection="3d")
    ax_nutrient = fig.add_subplot(132, projection="3d")
    ax_pheromone = fig.add_subplot(133, projection="3d")

    def update(frame):
        ax_agents.clear()
        ax_nutrient.clear()
        ax_pheromone.clear()

        snapshot = history_snapshots[frame]
        males, females, herms = _extract_positions_by_type(snapshot)
        n_m, n_f, n_h = _count_types(snapshot)
        total = n_m + n_f + n_h

        # ---------------------------------
        # Agents panel
        # ---------------------------------
        _draw_trails(
            ax_agents,
            frame,
            tracked_ids,
            agent_history,
            trail_length=trail_length,
        )

        if len(males) > 0:
            ax_agents.scatter(
                males[:, 0],
                males[:, 1],
                males[:, 2],
                s=20,
                c="blue",
                label="males",
                depthshade=True,
            )

        if len(females) > 0:
            ax_agents.scatter(
                females[:, 0],
                females[:, 1],
                females[:, 2],
                s=20,
                c="red",
                label="females",
                depthshade=True,
            )

        if len(herms) > 0:
            ax_agents.scatter(
                herms[:, 0],
                herms[:, 1],
                herms[:, 2],
                s=20,
                c="green",
                label="hermaphrodites",
                depthshade=True,
            )

        ax_agents.set_xlim(0, environment.x_size)
        ax_agents.set_ylim(0, environment.y_size)
        ax_agents.set_zlim(0, environment.z_size)
        ax_agents.set_xlabel("x")
        ax_agents.set_ylabel("y")
        ax_agents.set_zlabel("z")
        ax_agents.set_title(f"Agents - frame {frame}")

        info_text = (
            f"total: {total}\n"
            f"males: {n_m}\n"
            f"females: {n_f}\n"
            f"hermaphrodites: {n_h}"
        )

        ax_agents.text2D(
            0.02,
            0.98,
            info_text,
            transform=ax_agents.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

        handles, labels = ax_agents.get_legend_handles_labels()
        if len(handles) > 0:
            ax_agents.legend(loc="upper right")

        # ---------------------------------
        # Nutrient panel
        # ---------------------------------
        _plot_field_3d(
            ax_nutrient,
            nutrient_history[frame],
            environment,
            title="Nutrient field (environment)",
            threshold=nutrient_threshold,
            size_scale=60.0,
            cmap="YlGn",
            marker="s",
        )

        # ---------------------------------
        # Pheromone panel
        # ---------------------------------
        _plot_field_3d(
            ax_pheromone,
            pheromone_history[frame],
            environment,
            title="Pheromone field (environment)",
            threshold=pheromone_threshold,
            size_scale=120.0,
            cmap="plasma",
            marker="D",
        )

    anim = FuncAnimation(
        fig,
        update,
        frames=len(history_snapshots),
        interval=100,
        repeat=True,
    )

    writer = PillowWriter(fps=fps)
    anim.save(filename, writer=writer)
    plt.close(fig)