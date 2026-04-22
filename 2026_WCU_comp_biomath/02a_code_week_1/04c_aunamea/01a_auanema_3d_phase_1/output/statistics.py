from dataclasses import dataclass, field

from core.enums import SexType, LifeStage


@dataclass
class SimulationStatistics:
    time: list[float] = field(default_factory=list)
    total_population: list[int] = field(default_factory=list)

    males: list[int] = field(default_factory=list)
    females: list[int] = field(default_factory=list)
    hermaphrodites: list[int] = field(default_factory=list)

    juveniles: list[int] = field(default_factory=list)
    adults: list[int] = field(default_factory=list)
    reproductive_adults: list[int] = field(default_factory=list)

    births: list[int] = field(default_factory=list)
    deaths: list[int] = field(default_factory=list)

    def record(self, t, population, births, deaths):
        self.time.append(t)
        self.total_population.append(population.count_total())

        self.males.append(population.count_by_sex(SexType.MALE))
        self.females.append(population.count_by_sex(SexType.FEMALE))
        self.hermaphrodites.append(population.count_by_sex(SexType.HERMAPHRODITE))

        self.juveniles.append(population.count_by_stage(LifeStage.JUVENILE))
        self.adults.append(population.count_by_stage(LifeStage.ADULT))
        self.reproductive_adults.append(population.count_by_stage(LifeStage.REPRODUCTIVE_ADULT))

        self.births.append(births)
        self.deaths.append(deaths)