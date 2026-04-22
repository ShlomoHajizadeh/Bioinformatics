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


def _slice_index_from_position(environment, z_fraction=0.5):
    k = int(z_fraction * environment.grid_nz)
    k = max(0, min(environment.grid_nz - 1, k))
    return k


def _agents_in_slice(snapshot_agents, z_center, z_half_thickness):
    males_xy = []
    females_xy = []
    herms_xy = []

    for agent in snapshot_agents:
        if not agent.alive:
            continue

        if abs(agent.position[2] - z_center) > z_half_thickness:
            continue

        xy = agent.position[:2].copy()

        if agent.sex_type == SexType.MALE:
            males_xy.append(xy)
        elif agent.sex_type == SexType.FEMALE:
            females_xy.append(xy)
        else:
            herms_xy.append(xy)

    def as_array(lst):
        if len(lst) == 0:
            return np.empty((0, 2), dtype=float)
        return np.array(lst, dtype=float)

    return as_array(males_xy), as_array(females_xy), as_array(herms_xy)


def _plot_field_slice(ax, field_3d, environment, title, slice_k, cmap, vmin=None, vmax=None):
    field_slice = field_3d[:, :, slice_k].T

    im = ax.imshow(
        field_slice,
        origin="lower",
        extent=[0, environment.x_size, 0, environment.y_size],
        aspect="auto",
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
    )

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return im


def create_3d_animation_with_fields(
    history_snapshots,
    nutrient_history,
    pheromone_history,
    environment,
    filename="auanema_3d_animation.gif",
    fps=10,
    trail_length=12,
    max_trail_agents_per_type=3,
    nutrient_threshold=0.05,   # kept for compatibility
    pheromone_threshold=0.02,  # kept for compatibility
):
    if len(history_snapshots) == 0:
        print("No animation snapshots available.")
        return

    agent_history = _build_agent_history(history_snapshots)
    tracked_ids = _choose_trail_agents(
        history_snapshots,
        max_per_type=max_trail_agents_per_type,
    )

    slice_k = _slice_index_from_position(environment, z_fraction=0.5)
    z_center = (slice_k + 0.5) * environment.dz
    z_half_thickness = 0.5 * environment.dz

    # Fix color scaling across all frames for visual stability
    nutrient_vmin = 0.0
    nutrient_vmax = max(float(np.max(arr)) for arr in nutrient_history) if nutrient_history else 1.0
    pheromone_vmin = 0.0
    pheromone_vmax = max(float(np.max(arr)) for arr in pheromone_history) if pheromone_history else 1.0

    if nutrient_vmax <= nutrient_vmin:
        nutrient_vmax = nutrient_vmin + 1e-6
    if pheromone_vmax <= pheromone_vmin:
        pheromone_vmax = pheromone_vmin + 1e-6

    fig = plt.figure(figsize=(18, 6))
    ax_agents = fig.add_subplot(131, projection="3d")
    ax_nutrient = fig.add_subplot(132)
    ax_pheromone = fig.add_subplot(133)

    def update(frame):
        ax_agents.clear()
        ax_nutrient.clear()
        ax_pheromone.clear()

        snapshot = history_snapshots[frame]
        males, females, herms = _extract_positions_by_type(snapshot)
        n_m, n_f, n_h = _count_types(snapshot)
        total = n_m + n_f + n_h

        # Left panel: 3D agents
        _draw_trails(
            ax_agents,
            frame,
            tracked_ids,
            agent_history,
            trail_length=trail_length,
        )

        if len(males) > 0:
            ax_agents.scatter(
                males[:, 0], males[:, 1], males[:, 2],
                s=20, c="blue", label="males", depthshade=True
            )

        if len(females) > 0:
            ax_agents.scatter(
                females[:, 0], females[:, 1], females[:, 2],
                s=20, c="red", label="females", depthshade=True
            )

        if len(herms) > 0:
            ax_agents.scatter(
                herms[:, 0], herms[:, 1], herms[:, 2],
                s=20, c="green", label="hermaphrodites", depthshade=True
            )

        ax_agents.set_xlim(0, environment.x_size)
        ax_agents.set_ylim(0, environment.y_size)
        ax_agents.set_zlim(0, environment.z_size)
        ax_agents.set_xlabel("x")
        ax_agents.set_ylabel("y")
        ax_agents.set_zlabel("z")
        ax_agents.set_title(f"Agents in 3D - frame {frame}")

        info_text = (
            f"total: {total}\n"
            f"males: {n_m}\n"
            f"females: {n_f}\n"
            f"hermaphrodites: {n_h}\n"
            f"slice z ≈ {z_center:.1f}"
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

        # Agents near the slice
        males_xy, females_xy, herms_xy = _agents_in_slice(
            snapshot,
            z_center=z_center,
            z_half_thickness=z_half_thickness,
        )

        # Middle panel: nutrient slice
        _plot_field_slice(
            ax_nutrient,
            nutrient_history[frame],
            environment,
            title=f"Nutrient slice at z ≈ {z_center:.1f}",
            slice_k=slice_k,
            cmap="YlGn",
            vmin=nutrient_vmin,
            vmax=nutrient_vmax,
        )

        if len(males_xy) > 0:
            ax_nutrient.scatter(males_xy[:, 0], males_xy[:, 1], s=20, c="blue")
        if len(females_xy) > 0:
            ax_nutrient.scatter(females_xy[:, 0], females_xy[:, 1], s=20, c="red")
        if len(herms_xy) > 0:
            ax_nutrient.scatter(herms_xy[:, 0], herms_xy[:, 1], s=20, c="green")

        # Right panel: pheromone slice
        _plot_field_slice(
            ax_pheromone,
            pheromone_history[frame],
            environment,
            title=f"Pheromone slice at z ≈ {z_center:.1f}",
            slice_k=slice_k,
            cmap="plasma",
            vmin=pheromone_vmin,
            vmax=pheromone_vmax,
        )

        if len(males_xy) > 0:
            ax_pheromone.scatter(males_xy[:, 0], males_xy[:, 1], s=20, c="blue")
        if len(females_xy) > 0:
            ax_pheromone.scatter(females_xy[:, 0], females_xy[:, 1], s=20, c="red")
        if len(herms_xy) > 0:
            ax_pheromone.scatter(herms_xy[:, 0], herms_xy[:, 1], s=20, c="green")

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