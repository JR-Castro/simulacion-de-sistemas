import os.path
import sys
import time
from os import listdir, path
from os.path import abspath, isfile

import matplotlib.pyplot as plt
import numpy as np

from graph_pressure import calculate_wall_pressures, calculate_obstacle_pressures
from read_files import read_collisions, read_static_file


def compute_square_error(c, x_values, combined_mean):
    predicted = [c * x for x in x_values]
    squared_errors = [(p - m) ** 2 for p, m in zip(predicted, combined_mean)]
    return sum(squared_errors)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python graph_two.py <static_path> <outputs_path>")
        sys.exit(1)

    static_files_path = abspath(sys.argv[1])

    output_files_path = abspath(sys.argv[2])

    static_files = [os.path.join(static_files_path, f'test_{i}.txt') for i in [3, 6, 10]]
    # static_files.sort()

    output_files_prefixes = [f"test_{i}_" for i in [3, 6, 10]]
    output_files = [[f for f in listdir(output_files_path) if
                     isfile(path.join(output_files_path, f)) and f.startswith(prefix) and
                     f.endswith("_collisions.txt")] for prefix in output_files_prefixes]

    print(f"Static files: {static_files}")
    print(f"Output files: {output_files}")

    wall_press_mean = []
    wall_press_std = []
    obs_press_mean = []
    obs_press_std = []

    n = 0

    time_start = time.time()

    TIME_STEP = 0.01
    i = 0
    for static_file in static_files:
        static_data = read_static_file(os.path.join(static_files_path, static_file))
        n = static_data['N']
        collisions = [read_collisions(os.path.join(output_files_path, output_file)) for output_file in output_files[i]]
        wall_pressures = [[p['pressure'] for p in calculate_wall_pressures(static_data, c, TIME_STEP)] for c in
                          collisions]
        obstacle_pressures = [[p['pressure'] for p in calculate_obstacle_pressures(static_data, c, TIME_STEP)] for
                              c in
                              collisions]

        np_wall = np.array(wall_pressures)
        np_obs = np.array(obstacle_pressures)

        wall_mean = np.mean(np_wall, axis=(0, 1))
        wall_std = np.std(np_wall, axis=(0, 1))

        obs_mean = np.mean(np_obs, axis=(0, 1))
        obs_std = np.std(np_obs, axis=(0, 1))

        wall_press_mean.append(wall_mean)
        wall_press_std.append(wall_std)
        obs_press_mean.append(obs_mean)
        obs_press_std.append(obs_std)
        i += 1

    speed_values = [3 ** 2, 6 ** 2, 10 ** 2]
    x_values = [n * 0.5 * 1 * v for v in speed_values]

    # Combine the mean pressures of wall and obstacle
    combined_mean = [0.5 * (wall_press_mean[i] + obs_press_mean[i]) for i in range(len(wall_press_mean))]

    # Perform linear regression to fit the line f(x) = c*x
    numerator = sum(x * y for x, y in zip(x_values, combined_mean))
    denominator = sum(x ** 2 for x in x_values)
    c_fit = numerator / denominator

    print(f"Best c: {c_fit} * x")
    print(f"Error: {compute_square_error(c_fit, x_values, combined_mean)}")

    plt.errorbar(x_values, wall_press_mean, yerr=wall_press_std, fmt='o', capsize=5, label='Paredes')
    plt.errorbar(x_values, obs_press_mean, yerr=obs_press_std, fmt='o', capsize=5, label='Obstáculo')

    plt.plot(x_values, [c_fit * x for x in x_values], linestyle='--', label=f'f(x) = {c_fit:.2f}x', color='red')

    plt.xlabel("Energía Cinética (J)", fontsize=12)
    plt.ylabel("Presión (N/m)", fontsize=12)
    plt.legend(loc='upper left', shadow=True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.savefig("pressure_vs_speed.png", dpi=400)
    plt.clf()

    # Add a new plot that shows the square error based on the value of c, and how the one I chose is the minimum

    c_values = np.linspace(c_fit / 2, 3 * c_fit / 2, 1000)

    square_errors = [compute_square_error(c, x_values, combined_mean) for c in c_values]
    plt.plot(c_values, square_errors, label="Error cuadrático")
    plt.plot(c_fit, min(square_errors), linestyle='', marker='o', color='black', label=f"Mejor c")

    plt.axvline(x=c_fit, color='grey', linestyle='--')
    plt.axhline(y=min(square_errors), color='grey', linestyle='--')

    plt.xlabel("Valor de c", fontsize=12)
    plt.ylabel("Error cuadrático", fontsize=12)
    plt.legend(loc='upper left', shadow=True)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.savefig("square_error_vs_c_pressures.png", dpi=400)
    print(f"Total time: {time.time() - time_start}s")
