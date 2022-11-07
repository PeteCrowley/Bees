# Pcrowley
# 11/05/2022

"""
Day t=0 means January 1, 2022
"""

import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from date_helpers import day_to_date, date_to_day
import matplotlib.ticker as ticker

# Parameters
STARTING_POPULATION = 20000
STARTING_DATE = (2022, 8, 10)
DRONE_PERCENT = 10
DAYS = 1000
PRINT_SUMMARY = False


def drone_lifespan(day: int) -> int:
    """
    Calculates the lifespan of drone honeybees at a given time of year
    :param day: the time of year
    :return: the integer lifespan of a drone
    """
    return 20


def worker_lifespan(day: int) -> int:
    """
        Calculates the lifespan of worker honeybees at a given time of year
        :param day: the time of year
        :return: the integer lifespan of a worker
        """
    day_of_year = day % 365
    if day_of_year < 79 or day_of_year > 355:
        return 120
    if day_of_year < 172 or day_of_year > 266:
        return 45
    return 26


class BeePopulation:
    def __init__(self, initial_population, start_day):
        self.population_size = initial_population
        self.drones = initial_population // DRONE_PERCENT
        self.workers = self.population_size - self.drones
        self.day = start_day

    def new_bees(self) -> int:
        new_bees = 2000
        new_drones = (self.population_size + 2000) // DRONE_PERCENT - self.drones
        new_workers = 2000 - new_drones
        self.drones += new_drones
        self.workers += new_workers
        return new_bees

    def dead_bees(self) -> int:
        dead_workers = self.workers // worker_lifespan(self.day)
        dead_drones = self.drones // drone_lifespan(self.day)
        self.drones -= dead_drones
        self.workers -= dead_workers
        return dead_workers + dead_drones

    def population_change(self):
        return self.dead_bees() - self.new_bees()

    def step(self):
        self.population_size += self.new_bees() - self.dead_bees()
        self.day += 1

    def __str__(self) -> str:
        """
        Gets a string summary of the honeybee population demographic
        :return: a summary of the honeybee population
        """
        return "Date: " + str(day_to_date(self.day)) + "\nPopulation Size: " + str(self.population_size) + \
               "\nWorkers: " + str(self.workers) + "\nDrones: " + str(self.drones)


if __name__ == "__main__":
    Bees = BeePopulation(STARTING_POPULATION, date_to_day(STARTING_DATE)) # Initializing Population
    if PRINT_SUMMARY:
        print(Bees, end="\n\n")
    # Initializing lists for data collection
    day_list = [date_to_day(STARTING_DATE)]
    pop_size = [Bees.population_size]
    workers = [Bees.workers]
    drones = [Bees.drones]
    # Simulating the defined number of days
    for i in range(DAYS):
        Bees.step()
        # Add data from each step to lists
        day_list.append(Bees.day)
        pop_size.append(Bees.population_size)
        workers.append(Bees.workers)
        drones.append(Bees.drones)
        if PRINT_SUMMARY:
            print(Bees, end="\n\n")

    mdate_list = mdates.date2num([day_to_date(day_list[x]) for x in range(len(day_list))])  # Dates to matplotlib dates

    # Styling Graph
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set(xlabel="Date", ylabel="Number of Bees (thousands)", title="Bee Population")
    ax.legend(loc="upper right")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    plt.setp(ax.get_xticklabels(), rotation=90, fontsize=8)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1 if (DAYS < 1200) else round(DAYS/800)))
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / 1000))
    ax.yaxis.set_major_formatter(ticks_y)

    # Plotting Data
    ax.plot(mdate_list, pop_size, label="Population")
    plt.plot(mdate_list, workers, label="Workers")
    plt.plot(mdate_list, drones, label="Drones")

    # plt.savefig("./Images/SecondModel")
    plt.show()
