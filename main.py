# Pcrowley
# 11/05/2022

"""
Day t=0 means January 1, 2022
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import matplotlib.ticker as ticker
import random
import math

# Parameters
STARTING_POPULATION = 20000
STARTING_DATE = datetime.datetime(2022, 1, 10)
DRONE_PERCENT = 10
MAXIMUM_AVERAGE_LIFESPAN = 120
MINIMUM_AVERAGE_LIFESPAN = 15
LAST_BORN_DAY = datetime.datetime(year=2022, month=10, day=15)
MAX_NEW_BEES = 2000
QUEEN_LIFESPAN = 1200
QUEEN_LAYING_PEAK = 200
AGE_MATTERS = True
SWARMING = True
COMPLEX_SWARMING = True
SWARM_TIME = datetime.timedelta(days=14)
SWARM_SEASON_START_DAY = datetime.datetime(year=2022, month=4, day=15).timetuple().tm_yday
SWARM_SEASON_END_DAY = datetime.datetime(year=2022, month=5, day=31).timetuple().tm_yday
DAYS = 1500
DAY_STEP, HOUR_STEP, MINUTE_STEP = 0, 0, 30
FLOAT_DAY_STEP = DAY_STEP + HOUR_STEP/24 + MINUTE_STEP/1_440
TIME_STEP = datetime.timedelta(days=DAY_STEP, hours=HOUR_STEP, minutes=MINUTE_STEP)
PRINT_SUMMARY = False
DEAD_QUEEN_DAY = STARTING_DATE + datetime.timedelta(days=QUEEN_LIFESPAN)
MODEL_ITERATION = 10

def cubic_new_bees(date: datetime.datetime) -> float:
    if date.month > LAST_BORN_DAY.month or (date.month == LAST_BORN_DAY.month and date.day > LAST_BORN_DAY.day):
        return 0
    day_of_year = date.timetuple().tm_yday
    end_day = LAST_BORN_DAY.timetuple().tm_yday
    a = (-2 * end_day + math.sqrt(4 * (end_day ** 2) + 3 * (-end_day ** 2))) / -3
    b = MAX_NEW_BEES / (a * ((end_day - a) ** 2))
    return b * (end_day - day_of_year) * day_of_year ** 2


def quadratic_new_bees(date: datetime.datetime) -> float:
    if date.month > LAST_BORN_DAY.month or (date.month == LAST_BORN_DAY.month and date.day > LAST_BORN_DAY.day):
        return 0
    day_of_year = date.timetuple().tm_yday
    end_day = LAST_BORN_DAY.timetuple().tm_yday
    a = (end_day ** 2) / (4 * MAX_NEW_BEES)
    return -(day_of_year * (day_of_year - end_day)) / a


def drone_lifespan(date: datetime.datetime) -> int:
    """
    Calculates the lifespan of drone honeybees at a given time of year
    :param date: the date
    :return: the integer lifespan of a drone90-
    """
    return 20


def worker_lifespan(date: datetime.datetime) -> int:
    """
        Calculates the lifespan of worker honeybees at a given time of year
        :param date: the date
        :return: the integer lifespan of a worker
        """
    day_of_year = date.timetuple().tm_yday
    if day_of_year < 79 or day_of_year > 355:
        return 120
    if day_of_year < 172 or day_of_year > 266:
        return 45
    return 26


def queen_productivity(date: datetime.datetime) -> float:
    days_old = (date - STARTING_DATE).days
    b = QUEEN_LIFESPAN - 2 * QUEEN_LAYING_PEAK
    m = 1 / ((QUEEN_LAYING_PEAK - QUEEN_LIFESPAN) * (QUEEN_LAYING_PEAK + b))
    productivity = m * (days_old - QUEEN_LIFESPAN) * (days_old + b)
    return productivity if productivity > 0 else 0




def sine_worker_lifespan(date: datetime.datetime) -> float:
    """
        Calculates the lifespan of worker honeybees at a given time of year
        :param date: the date
        :return: the integer lifespan of a worker
        """
    day_of_year = date.timetuple().tm_yday
    a = MAXIMUM_AVERAGE_LIFESPAN * 2 + 15
    return a * math.cos((2 * math.pi * (day_of_year - 35)) / 365) + (a + MINIMUM_AVERAGE_LIFESPAN)


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
        if self.date.month < 3:
            self.next_swarm_date = choose_swarm_day(self.date.year)
        else:
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
        dead_workers = FLOAT_DAY_STEP * (self.workers // sine_worker_lifespan(self.date))
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



    def step(self) -> None:
        if self.swarming:
            self.population_size -= self.dead_bees()
            if self.date >= self.end_swarm_date:
                self.swarming = False
                self.end_swarm_date = self.next_swarm_date + SWARM_TIME
        else:
            self.population_size += self.new_bees() - self.dead_bees()
        self.date += TIME_STEP
        if SWARMING and self.date >= self.next_swarm_date:
            self.swarm()

    def __str__(self) -> str:
        """
        Gets a string summary of the honeybee population demographic
        :return: a summary of the honeybee population
        """
        return "Date: " + str(self.date) + "\nPopulation Size: " + str(round(self.population_size)) + \
               "\nWorkers: " + str(round(self.workers)) + "\nDrones: " + str(round(self.drones))


if __name__ == "__main__":
    Bees = BeePopulation(STARTING_POPULATION, STARTING_DATE)    # Initializing Population
    if PRINT_SUMMARY:
        print(Bees, end="\n\n")
    # Initializing lists for data collection
    date_list = [STARTING_DATE]
    pop_size = [Bees.population_size]
    workers = [Bees.workers]
    drones = [Bees.drones]
    # Simulating the defined number of days
    for i in range(round(DAYS/FLOAT_DAY_STEP)):
        Bees.step()
        # Add data from each step to lists
        date_list.append(Bees.date)
        pop_size.append(Bees.population_size)
        workers.append(Bees.workers)
        drones.append(Bees.drones)
        if PRINT_SUMMARY:
            print(Bees, end="\n\n")

    mdate_list = mdates.date2num(date_list)  # Dates to matplotlib dates

    # Styling Graph
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set(xlabel="Date", ylabel="Number of Bees (thousands)", title="Bee Population")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    plt.setp(ax.get_xticklabels(), rotation=90, fontsize=8)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1 if (DAYS < 1200) else round(DAYS/800)))
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / 1000))
    ax.yaxis.set_major_formatter(ticks_y)

    # Plotting Data
    ax.plot(mdate_list, pop_size, label="Total Population")
    ax.plot(mdate_list, workers, label="Workers")
    ax.plot(mdate_list, drones, label="Drones")
    ax.axvline(x=DEAD_QUEEN_DAY, label="The Queen Dies", color="red")

    # Legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0,
                     box.width*1.05, box.height])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
              fancybox=True, shadow=True, ncol=5)

    plt.savefig("./Images/Model_" + str(MODEL_ITERATION))
    plt.show()
