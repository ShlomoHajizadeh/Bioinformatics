from config.config import MAX_AGE, BIRD_STARVE_AFTER, BEAR_STARVE_NT_AFTER, BEAR_STARVE_E_AFTER


def apply_mortality(agents):
    """
    Apply age and starvation mortality.

    Returns
    -------
    dict
        Death counts by cause and species.
    """
    death_stats = {
        "age_NT": 0,
        "age_IT": 0,
        "age_B": 0,
        "age_P": 0,
        "age_E": 0,
        "starve_B": 0,
        "starve_P": 0
    }

    for agent in agents:
        if not agent.alive:
            continue

        if agent.age > MAX_AGE[agent.species]:
            agent.alive = False
            death_stats["age_" + agent.species] += 1
            continue

        if agent.species == "P":
            if agent.steps_since_nt_meal > BIRD_STARVE_AFTER:
                agent.alive = False
                death_stats["starve_P"] += 1
                continue

        if agent.species == "B":
            no_trout_recently = agent.steps_since_bear_nt_meal > BEAR_STARVE_NT_AFTER
            no_elk_recently = agent.steps_since_bear_e_meal > BEAR_STARVE_E_AFTER

            if no_trout_recently and no_elk_recently:
                agent.alive = False
                death_stats["starve_B"] += 1
                continue

    return death_stats