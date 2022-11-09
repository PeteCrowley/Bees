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

# Parameters
STARTING_POPULATION = 20000
STARTING_DATE = datetime.date(2022, 8, 10)
DRONE_PERCENT = 10
DAYS = 1000
PRINT_SUMMARY = False
MODEL_ITERATION = 4


def drone_lifespan(date: datetime.date) -> int:
    """
    Calculates the lifespan of drone honeybees at a given time of year
    :param date: the date
    :return: the integer lifespan of a drone
    """
    return 20


def worker_lifespan(date: datetime.date) -> int:
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


def choose_swarm_day(year: int) -> datetime.date:
    if year % 4 == 0:
        min_day = 60
    else:
        min_day = 59
    if year % 4 == 0:
        max_day = 151
    else:
        max_day = 150
    swarm_day = random.randint(min_day, max_day)
    return datetime.date(year, 1, 1) + datetime.timedelta(days=swarm_day)


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

    def new_bees(self) -> int:
        new_bees = 2000
        new_drones = (self.population_size + 2000) // DRONE_PERCENT - self.drones
        new_workers = 2000 - new_drones
        self.drones += new_drones
        self.workers += new_workers
        return new_bees

    def dead_bees(self) -> int:
        dead_workers = self.workers // worker_lifespan(self.date)
        dead_drones = self.drones // drone_lifespan(self.date)
        self.drones -= dead_drones
        self.workers -= dead_workers
        return dead_workers + dead_drones

    def population_change(self):
        return self.dead_bees() - self.new_bees()

    def swarm(self):
        self.population_size //= 2
        self.drones //= 2
        self.workers //= 2
        self.next_swarm_date = choose_swarm_day(self.date.year + 1)

    def step(self):
        self.population_size += self.new_bees() - self.dead_bees()
        self.date += datetime.timedelta(days=1)
        if self.date == self.next_swarm_date:
            self.swarm()

    def __str__(self) -> str:
        """
        Gets a string summary of the honeybee population demographic
        :return: a summary of the honeybee population
        """
        return "Date: " + str(self.date) + "\nPopulation Size: " + str(self.population_size) + \
               "\nWorkers: " + str(self.workers) + "\nDrones: " + str(self.drones)


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
    for i in range(DAYS):
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
    plt.plot(mdate_list, workers, label="Workers")
    plt.plot(mdate_list, drones, label="Drones")

    # Legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0,
                     box.width*1.05, box.height])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
              fancybox=True, shadow=True, ncol=5)

    plt.savefig("./Images/Model_" + str(MODEL_ITERATION))
    plt.show()
