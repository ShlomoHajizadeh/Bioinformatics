from core.enums import LifeStage


def update_life_stage(agent, config):
    if agent.age < config.JUVENILE_AGE_THRESHOLD:
        agent.life_stage = LifeStage.JUVENILE
    elif agent.age < config.ADULT_AGE_THRESHOLD:
        agent.life_stage = LifeStage.ADULT
    else:
        agent.life_stage = LifeStage.REPRODUCTIVE_ADULT


def age_agent(agent, dt, config):
    agent.age += dt
    agent.step_birth_clock(dt)
    update_life_stage(agent, config)


def age_all_agents(population, dt, config):
    for agent in population.alive_agents():
        age_agent(agent, dt, config)