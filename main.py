# Pcrowley
# 11/05/2022

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Bee_Model import *
import Bee_Model


def run_simulation(print_summary=False, save_fig=False):
    bees = BeePopulation(STARTING_POPULATION, STARTING_DATE)  # Initializing Population
    if print_summary:
        print(bees, end="\n\n")
    # Initializing lists for data collection
    date_list = [STARTING_DATE]
    pop_size = [bees.population_size]
    workers = [bees.workers]
    drones = [bees.drones]
    # Simulating the defined number of days
    for i in range(round(DAYS / FLOAT_DAY_STEP)):
        bees.step()
        # Add data from each step to lists
        date_list.append(bees.date)
        pop_size.append(bees.population_size)
        workers.append(bees.workers)
        drones.append(bees.drones)
        if print_summary:
            print(bees, end="\n\n")
    mdate_list = mdates.date2num(date_list)  # Dates to matplotlib dates

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set(xlabel="Date", ylabel="Number of Bees (thousands)", title="Bee Population")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    plt.setp(ax.get_xticklabels(), rotation=90, fontsize=8)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1 if (DAYS < 1200) else round(DAYS / 800)))
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
                     box.width * 1.05, box.height])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
              fancybox=True, shadow=True, ncol=5)
    if save_fig:
        plt.savefig("./Images/Model_" + str(MODEL_ITERATION))
    plt.show()


def get_simulation_list():
    bees = BeePopulation(Bee_Model.STARTING_POPULATION, STARTING_DATE)  # Initializing Population
    # Initializing lists for data collection
    date_list = []
    percent_pop_change_list = []
    # Simulating the defined number of days
    for i in range(round(DAYS / FLOAT_DAY_STEP)):
        pop_size = bees.population_size
        percent_pop_change_list.append((bees.step() / FLOAT_DAY_STEP) / pop_size * 100)
        date_list.append(bees.date)
    return date_list, percent_pop_change_list


def sensitivity_analysis_1():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set(xlabel="Date", ylabel="Percent Difference in Population Change Per Day", title="Bee Population")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    plt.setp(ax.get_xticklabels(), rotation=90, fontsize=8)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1 if (DAYS < 1300) else round(DAYS / 800)))

    dates, l1 = get_simulation_list()
    dates = mdates.date2num(dates)

    Bee_Model.MAXIMUM_AVERAGE_LIFESPAN *= 1.1
    max_lifespan = get_simulation_list()[1]
    max_lifespan_difference = [max_lifespan[x] - l1[x] for x in range(len(dates))]
    Bee_Model.MAXIMUM_AVERAGE_LIFESPAN /= 1.1

    Bee_Model.MINIMUM_AVERAGE_LIFESPAN *= 1.1
    min_lifespan = get_simulation_list()[1]
    min_lifespan_difference = [min_lifespan[x] - l1[x] for x in range(len(dates))]
    Bee_Model.MINIMUM_AVERAGE_LIFESPAN /= 1.1

    Bee_Model.DRONE_PERCENT *= 1.1
    drone_percent = get_simulation_list()[1]
    drone_percent_difference = [drone_percent[x] - l1[x] for x in range(len(dates))]
    Bee_Model.DRONE_PERCENT /= 1.1

    Bee_Model.MAX_NEW_BEES *= 1.1
    max_new_bees = get_simulation_list()[1]
    max_new_bees_difference = [max_new_bees[x] - l1[x] for x in range(len(dates))]
    Bee_Model.MAX_NEW_BEES /= 1.1

    Bee_Model.STARTING_POPULATION *= 1.1
    pop_size = get_simulation_list()[1]
    pop_size_difference = [pop_size[x] - l1[x] for x in range(len(dates))]
    Bee_Model.STARTING_POPULATION /= 1.1

    # Plotting Data
    ax.plot(dates, max_lifespan_difference, label="Max Lifespan")
    ax.plot(dates, min_lifespan_difference, label="Min Lifespan")
    ax.plot(dates, drone_percent_difference, label="Drone Percent")
    ax.plot(dates, max_new_bees_difference, label="Max New Bees")
    ax.plot(dates, pop_size_difference, label="Pop Size")
    # Legend
    ax.legend(loc="upper right")
    plt.savefig("Images/Sensitivity_Analysis_1")
    plt.show()


def sensitivity_analysis_2():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set(xlabel="Date", ylabel="Percent Difference in Population Change Per Day", title="Bee Population")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    plt.setp(ax.get_xticklabels(), rotation=90, fontsize=8)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1 if (DAYS < 1300) else round(DAYS / 800)))

    dates, l1 = get_simulation_list()
    dates = mdates.date2num(dates)

    old_bee_day = Bee_Model.LAST_BORN_DAY
    last_bee_day = round(Bee_Model.LAST_BORN_DAY.timetuple().tm_yday * 1.1)
    Bee_Model.LAST_BORN_DAY = datetime.datetime(2022, 1, 1) + datetime.timedelta(last_bee_day)
    end_date = get_simulation_list()[1]
    end_date_difference = [end_date[x] - l1[x] for x in range(len(dates))]
    Bee_Model.LAST_BORN_DAY = old_bee_day

    Bee_Model.QUEEN_LIFESPAN *= 1.1
    queen_life = get_simulation_list()[1]
    queen_life_difference = [queen_life[x] - l1[x] for x in range(len(dates))]
    Bee_Model.QUEEN_LIFESPAN /= 1.1

    Bee_Model.QUEEN_LAYING_PEAK *= 1.1
    queen_peak = get_simulation_list()[1]
    queen_peak_difference = [queen_peak[x] - l1[x] for x in range(len(dates))]
    Bee_Model.QUEEN_LAYING_PEAK /= 1.1

    # Plotting Data
    ax.plot(dates, end_date_difference, label="Last Bee Date")
    ax.plot(dates, queen_life_difference, label="Queen Lifespan")
    ax.plot(dates, queen_peak_difference, label="Queen Peak")
    # Legend
    ax.legend(loc="upper right")

    plt.savefig("Images/Sensitivity_Analysis_2")
    plt.show()


if __name__ == "__main__":
    run_simulation(save_fig=False)

