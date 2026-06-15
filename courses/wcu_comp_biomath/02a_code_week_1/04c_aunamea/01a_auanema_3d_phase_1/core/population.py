from typing import List

from core.agent import NematodeAgent
from core.enums import SexType, LifeStage


class Population:
    def __init__(self, agents: List[NematodeAgent] | None = None):
        self.agents = agents if agents is not None else []

    def add_agent(self, agent: NematodeAgent) -> None:
        self.agents.append(agent)

    def add_agents(self, agents: List[NematodeAgent]) -> None:
        self.agents.extend(agents)

    def alive_agents(self) -> List[NematodeAgent]:
        return [a for a in self.agents if a.alive]

    def remove_dead(self) -> int:
        before = len(self.agents)
        self.agents = [a for a in self.agents if a.alive]
        return before - len(self.agents)

    def count_total(self) -> int:
        return len(self.alive_agents())

    def count_by_sex(self, sex_type: SexType) -> int:
        return sum(1 for a in self.alive_agents() if a.sex_type == sex_type)

    def count_by_stage(self, life_stage: LifeStage) -> int:
        return sum(1 for a in self.alive_agents() if a.life_stage == life_stage)