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
    """
    Build a dictionary:
        agent_id -> list of positions over frames (or None if absent in a frame)

    This allows us to draw trails for agents that persist across frames.
    """
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
    """
    Select a few agents of each type from the first frame for trails.
    """
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
    """
    Draw short trails for a selected set of agents.
    """
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


def create_3d_animation(
    history_snapshots,
    environment,
    filename="auanema_3d_animation.gif",
    fps=10,
    trail_length=12,
    max_trail_agents_per_type=3,
):
    if len(history_snapshots) == 0:
        print("No animation snapshots available.")
        return

    agent_history = _build_agent_history(history_snapshots)
    tracked_ids = _choose_trail_agents(
        history_snapshots,
        max_per_type=max_trail_agents_per_type,
    )

    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")

    def update(frame):
        ax.clear()

        snapshot = history_snapshots[frame]
        males, females, herms = _extract_positions_by_type(snapshot)
        n_m, n_f, n_h = _count_types(snapshot)
        total = n_m + n_f + n_h

        # draw short trails first
        _draw_trails(
            ax,
            frame,
            tracked_ids,
            agent_history,
            trail_length=trail_length,
        )

        # clear colors by type
        if len(males) > 0:
            ax.scatter(
                males[:, 0], males[:, 1], males[:, 2],
                s=20,
                c="blue",
                label="males",
                depthshade=True,
            )

        if len(females) > 0:
            ax.scatter(
                females[:, 0], females[:, 1], females[:, 2],
                s=20,
                c="red",
                label="females",
                depthshade=True,
            )

        if len(herms) > 0:
            ax.scatter(
                herms[:, 0], herms[:, 1], herms[:, 2],
                s=20,
                c="green",
                label="hermaphrodites",
                depthshade=True,
            )

        ax.set_xlim(0, environment.x_size)
        ax.set_ylim(0, environment.y_size)
        ax.set_zlim(0, environment.z_size)

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_title(f"Auanema 3D population - frame {frame}")

        # text overlay with current counts
        info_text = (
            f"frame: {frame}\n"
            f"total: {total}\n"
            f"males: {n_m}\n"
            f"females: {n_f}\n"
            f"hermaphrodites: {n_h}"
        )

        ax.text2D(
            0.02,
            0.98,
            info_text,
            transform=ax.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

        handles, labels = ax.get_legend_handles_labels()
        if len(handles) > 0:
            ax.legend(loc="upper right")

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