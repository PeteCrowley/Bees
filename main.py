# Pcrowley
# 11/05/2022

"""
Day t=0 means January 1, 2022
"""

import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from date_helpers import day_to_date, date_to_day


STARTING_POPULATION = 20000
STARTING_DATE = (2022, 8, 10)
DRONE_PERCENT = 10


def drone_lifespan(day: int) -> int:
    return 20


def worker_lifespan(day: int) -> int:
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
        Gets a string summary of the population demographic
        :return: a summary of the population
        """
        return "Date: " + str(day_to_date(self.day)) + "\nPopulation Size: " + str(self.population_size) + "\nWorkers: " + \
               str(self.workers) + "\nDrones: " + str(self.drones)


if __name__ == "__main__":
    Bees = BeePopulation(STARTING_POPULATION, date_to_day(STARTING_DATE))
    print(Bees)
    print()
    day_list = [0]
    pop_size = [Bees.population_size]
    workers = [Bees.workers]
    drones = [Bees.drones]
    for i in range(1000):
        Bees.step()
        day_list.append(Bees.day)
        pop_size.append(Bees.population_size)
        workers.append(Bees.workers)
        drones.append(Bees.drones)
        print(Bees)
        print()

    date_list = [day_to_date(day_list[x]) for x in range(len(day_list))]
    mdate_list = mdates.date2num(date_list)
    x_list = mdate_list
    # date_list = mdates.drange(start_date, )
    month_locator = mdates.MonthLocator(interval=1)
    # Make a pretty graph
    plt.title("Bee Population")
    plt.xlabel("Day of Year")
    plt.ylabel("Number of Gees")
    plt.plot(x_list, pop_size, label="Population")
    plt.plot(x_list, workers, label="Workers")
    plt.plot(x_list, drones, label="Drones")
    plt.legend(loc="upper right")
    plt.savefig("./Images/SecondModel")
    plt.show()
