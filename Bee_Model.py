# Pcrowley
# 11/05/2022

import datetime
import matplotlib.ticker as ticker
import random
import math

# Parameters
STARTING_POPULATION = 20000
STARTING_DATE = datetime.datetime(2021, 12, 31)
DRONE_PERCENT = 10
MAXIMUM_AVERAGE_LIFESPAN = 120
MINIMUM_AVERAGE_LIFESPAN = 15
LAST_BORN_DAY = datetime.datetime(year=2022, month=10, day=15)
MAX_NEW_BEES = 3000
QUEEN_LIFESPAN = 1000
QUEEN_LAYING_PEAK = 200
AGE_MATTERS = True
SWARMING = True
COMPLEX_SWARMING = True
SWARM_TIME = datetime.timedelta(days=14)
SWARM_SEASON_START_DAY = datetime.datetime(year=2022, month=4, day=15).timetuple().tm_yday
SWARM_SEASON_END_DAY = datetime.datetime(year=2022, month=5, day=31).timetuple().tm_yday
DAYS = QUEEN_LIFESPAN + 100
DAY_STEP, HOUR_STEP, MINUTE_STEP = 0, 1, 0
FLOAT_DAY_STEP = DAY_STEP + HOUR_STEP/24 + MINUTE_STEP/1_440
TIME_STEP = datetime.timedelta(days=DAY_STEP, hours=HOUR_STEP, minutes=MINUTE_STEP)
DEAD_QUEEN_DAY = STARTING_DATE + datetime.timedelta(days=QUEEN_LIFESPAN)
MODEL_ITERATION = 11


def cubic_new_bees(date: datetime.datetime) -> float:
    if date.month > LAST_BORN_DAY.month or (date.month == LAST_BORN_DAY.month and date.day > LAST_BORN_DAY.day):
        return 0
    day_of_year = date.timetuple().tm_yday
    end_day = LAST_BORN_DAY.timetuple().tm_yday
    a = 2/3*end_day
    b = MAX_NEW_BEES / (a ** 2 * (end_day - a))
    return b * (end_day - day_of_year) * day_of_year ** 2


def queen_productivity(date: datetime.datetime) -> float:
    days_old = (date - STARTING_DATE).days
    b = QUEEN_LIFESPAN - 2 * QUEEN_LAYING_PEAK
    m = 1 / ((QUEEN_LAYING_PEAK - QUEEN_LIFESPAN) * (QUEEN_LAYING_PEAK + b))
    productivity = m * (days_old - QUEEN_LIFESPAN) * (days_old + b)
    return productivity if productivity > 0 else 0


def drone_lifespan(date: datetime.datetime) -> int:
    return 20


def cosine_worker_lifespan(date: datetime.datetime) -> float:
    day_of_year = date.timetuple().tm_yday
    a = (MAXIMUM_AVERAGE_LIFESPAN - MINIMUM_AVERAGE_LIFESPAN) / 2
    return a * math.cos((2 * math.pi * (day_of_year-35)) / 365) + (a + MINIMUM_AVERAGE_LIFESPAN)


def choose_swarm_day(year: int) -> datetime.datetime:
    swarm_day = random.randint(SWARM_SEASON_START_DAY, SWARM_SEASON_END_DAY)
    return datetime.datetime(year, 1, 1) + datetime.timedelta(days=swarm_day)


class BeePopulation:
    def __init__(self, initial_population, start_date):
        self.population_size = initial_population
        self.drones = initial_population // DRONE_PERCENT
        self.workers = self.population_size - self.drones
        self.date = start_date
        self.has_swarmed = False
        self.next_swarm_date = choose_swarm_day(self.date.year + 1)
        if COMPLEX_SWARMING:
            self.end_swarm_date = self.next_swarm_date + SWARM_TIME
        self.swarming = False

    def new_bees(self) -> float:
        new_bees = cubic_new_bees(self.date) * FLOAT_DAY_STEP
        if AGE_MATTERS:
            new_bees *= queen_productivity(self.date)
        new_drones = (self.population_size + new_bees) // DRONE_PERCENT - self.drones
        if new_drones > new_bees:
            new_drones = new_bees
        new_workers = new_bees - new_drones
        self.drones += new_drones
        self.workers += new_workers
        return new_bees

    def dead_bees(self) -> float:
        dead_workers = FLOAT_DAY_STEP * (self.workers // cosine_worker_lifespan(self.date))
        dead_drones = FLOAT_DAY_STEP * (self.drones // drone_lifespan(self.date))
        self.drones -= dead_drones
        self.workers -= dead_workers
        return dead_workers + dead_drones

    def swarm(self) -> None:
        self.population_size //= 2
        self.drones //= 2
        self.workers //= 2
        self.next_swarm_date = choose_swarm_day(self.date.year + 1)
        if COMPLEX_SWARMING:
            self.swarming = True

    def step(self) -> float:
        if self.swarming:
            pop_change = -1 * self.dead_bees()
            if self.date >= self.end_swarm_date:
                self.swarming = False
                self.end_swarm_date = self.next_swarm_date + SWARM_TIME
        else:
            pop_change = self.new_bees() - self.dead_bees()
        self.population_size += pop_change
        self.date += TIME_STEP
        if SWARMING and self.date >= self.next_swarm_date:
            self.swarm()
        return pop_change


    def __str__(self) -> str:
        """
        Gets a string summary of the honeybee population demographic
        :return: a summary of the honeybee population
        """
        return "Date: " + str(self.date) + "\nPopulation Size: " + str(round(self.population_size)) + \
               "\nWorkers: " + str(round(self.workers)) + "\nDrones: " + str(round(self.drones))

