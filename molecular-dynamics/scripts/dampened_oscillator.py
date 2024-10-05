import math
import time

import matplotlib.pyplot as plt
import pandas
import pandas as pd
from matplotlib import rcParams

from graph_constants import formatter, FONT, DPI, set_axis_formatter

K = 10 ** 4
MAX_TIME = 5
MASS = 70
GAMMA = 100
R0 = 1
AMPLITUDE = 1
V0 = -AMPLITUDE * GAMMA / (2 * MASS)

RUNS = range(2, 7)
GRAPH_RUN = 3

ALGORITHMS = ['Verlet', 'Beeman', 'Gear']
COLORS = {
    'Verlet': 'blue',
    'Beeman': 'orange',
    'Gear': 'green'
}


def calc_solution(t):
    return AMPLITUDE * math.exp(- GAMMA / (2 * MASS) * t) * math.cos(
        math.sqrt(K / MASS - GAMMA ** 2 / (4 * MASS ** 2)) * t)


def calc_mean_cuadratic_error(solution, aproximate):
    error = 0
    for i in range(len(aproximate)):
        error += (aproximate[i] - solution[i]) ** 2
    return error / len(aproximate)

def get_files(integrator):
    return [f'output{integrator}_{i}.txt' for i in RUNS]


if __name__ == '__main__':
    start_time = time.time()
    # Load the data
    data_verlet = pd.read_csv(f'outputVerlet_{GRAPH_RUN}.txt')
    data_beeman = pd.read_csv(f'outputBeeman_{GRAPH_RUN}.txt')
    data_gear = pd.read_csv(f'outputGear_{GRAPH_RUN}.txt')

    data_solution = pd.DataFrame()
    data_solution['time'] = data_gear['time']
    data_solution['position'] = data_solution['time'].apply(calc_solution)

    # Calculate error
    error_verlet = calc_mean_cuadratic_error(data_solution['position'], data_verlet['position'])
    error_beeman = calc_mean_cuadratic_error(data_solution['position'], data_beeman['position'])
    error_gear = calc_mean_cuadratic_error(data_solution['position'], data_gear['position'])

    # print(data_beeman)

    # Filter the data to show only the last second
    data_verlet_filter = data_verlet
    data_beeman_filter = data_beeman
    data_gear_filter = data_gear
    data_solution_filter = data_solution

    # Plot the data
    plt.plot(data_verlet_filter['time'], data_verlet_filter['position'],
             label=f'Verlet E:{formatter(error_verlet, None)}', linestyle='-', color=COLORS['Verlet'])

    plt.plot(data_beeman_filter['time'], data_beeman_filter['position'],
             label=f'Beeman E:{formatter(error_beeman, None)}', linestyle='-', color=COLORS['Beeman'])

    plt.plot(data_gear_filter['time'], data_gear_filter['position'],
             label=f'Gear E:{formatter(error_gear, None)}', linestyle='-', color=COLORS['Gear'])

    plt.plot(data_solution_filter['time'], data_solution_filter['position'], label='Solución', linestyle='--')

    plt.xlabel('Tiempo (s)', fontdict=FONT)
    plt.ylabel('Posición (m)', fontdict=FONT)
    plt.legend(loc='lower right')
    plt.savefig('position_vs_time.png', dpi=DPI)

    plt.xlim(3.2, 3.3)
    plt.ylim(0, 0.1)
    plt.savefig('position_vs_time_zoom.png', dpi=DPI)
    plt.clf()

    fig, ax = plt.subplots()

    default_size = rcParams['lines.markersize'] ** 2
    print(default_size)

    dts = []
    err_verlet = []
    err_beeman = []
    err_gear = []

    for v_f, b_f, g_f in zip(*[get_files(integrator) for integrator in ALGORITHMS]):
        print(v_f, b_f, g_f)
        v_df = pandas.read_csv(v_f)
        b_df = pandas.read_csv(b_f)
        g_df = pandas.read_csv(g_f)

        steps = v_df['time']
        solution = [calc_solution(t) for t in steps]
        err_verlet.append(calc_mean_cuadratic_error(solution, v_df['position']))
        err_beeman.append(calc_mean_cuadratic_error(solution, b_df['position']))
        err_gear.append(calc_mean_cuadratic_error(solution, g_df['position']))
        dts.append(steps[1] - steps[0])

    ax.scatter(dts, err_verlet, s=default_size, label='Verlet', facecolors='none', edgecolors='blue')
    ax.scatter(dts, err_beeman, s=default_size, label='Beeman', facecolors='none', edgecolors='orange')
    ax.scatter(dts, err_gear, s=default_size, label='Gear', facecolors='none', edgecolors='green')
    ax.plot(dts, err_verlet, linestyle='-', color='blue')
    ax.plot(dts, err_beeman, linestyle='-', color='orange')
    ax.plot(dts, err_gear, linestyle='-', color='green')

    ax.set_xlabel('dt (s)', fontdict=FONT)
    ax.set_ylabel('Error Cuadrático Medio', fontdict=FONT)
    set_axis_formatter(ax)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')

    # Set major and minor ticks for both axes
    # ax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs='auto', numticks=10))
    # ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[2, 3, 4, 5, 6, 7, 8, 9], numticks=10))  # Minor ticks

    # Grid
    # ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.savefig('error_vs_dt.png', dpi=DPI)

    print(f'--- {time.time() - start_time} seconds ---')
