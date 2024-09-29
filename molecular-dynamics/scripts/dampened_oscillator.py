import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker

K = 10 ** 4
MAX_TIME = 5
MASS = 70
GAMMA = 100
R0 = 1
AMPLITUDE = 1
V0 = -AMPLITUDE * GAMMA / (2 * MASS)


# Define a custom formatter
def formatter(value, pos):
    exponent = int(np.floor(np.log10(abs(value)))) if value != 0 else 0
    coeff = value / 10 ** exponent
    return f'${coeff:.2f} \\times 10^{{{exponent}}}$'


def calc_solution(t):
    return AMPLITUDE * math.exp(- GAMMA / (2 * MASS) * t) * math.cos(
        math.sqrt(K / MASS - GAMMA ** 2 / (4 * MASS ** 2)) * t)


def calc_mean_cuadratic_error(solution, aproximate):
    error = 0
    for i in range(len(aproximate)):
        error += (aproximate[i] - solution[i]) ** 2
    return error / len(aproximate)


if __name__ == '__main__':
    # Load the data
    data_verlet = pd.read_csv('outputVerlet_6.txt')
    data_beeman = pd.read_csv('outputBeeman_6.txt')
    data_gear = pd.read_csv('outputGear_6.txt')

    data_solution = pd.DataFrame()
    data_solution['time'] = data_beeman['time']
    data_solution['position'] = data_solution['time'].apply(calc_solution)

    # Calculate error
    error_verlet = calc_mean_cuadratic_error(data_solution['position'], data_verlet['position'])
    error_beeman = calc_mean_cuadratic_error(data_solution['position'], data_beeman['position'])
    error_gear = calc_mean_cuadratic_error(data_solution['position'], data_gear['position'])

    # print(data_beeman)

    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 14}

    # Filter the data to show only the last second
    data_verlet_filter = data_verlet[data_verlet['time'] > 4.98]
    data_beeman_filter = data_beeman[data_beeman['time'] > 4.98]
    data_gear_filter = data_gear[data_gear['time'] > 4.98]
    data_solution_filter = data_solution[data_solution['time'] > 4.98]

    # Plot the data
    plt.plot(data_verlet_filter['time'], data_verlet_filter['position'], label=f'Verlet E:{formatter(error_verlet, None)}', marker='.',
             linestyle='-')
    plt.plot(data_beeman_filter['time'], data_beeman_filter['position'], label=f'Beeman E:{formatter(error_beeman, None)}', marker='.',
             linestyle='-')
    plt.plot(data_gear_filter['time'], data_gear_filter['position'], label=f'Gear E:{formatter(error_gear, None)}', marker='.', linestyle='-')
    plt.plot(data_solution_filter['time'], data_solution_filter['position'], label='Solución', linestyle='--')
    plt.xlabel('Tiempo (s)', fontdict=font)
    plt.ylabel('Posición (m)', fontdict=font)
    plt.legend(loc='lower right')
    plt.savefig('position_vs_time.png', dpi=400)
    plt.clf()

    fig, ax = plt.subplots()

    for integrator in ['Verlet', 'Beeman', 'Gear']:
        errors = []
        steps = []
        for i in range(1, 8):
            data = pd.read_csv(f'output{integrator}_{i}.txt')
            error = calc_mean_cuadratic_error(data_solution['position'], data['position'])
            steps.append(i)
            errors.append(error)

        ax.plot([0.1 ** step for step in steps], errors, label=f'{integrator}', marker='o', linestyle='--')

    ax.set_xlabel('dt (s)', fontdict=font)
    ax.set_ylabel('Error Cuadrático Medio', fontdict=font)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')

    plt.savefig('error_vs_dt.png', dpi=400)




