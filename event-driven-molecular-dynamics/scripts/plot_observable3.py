import re
import sys
import time
from collections import defaultdict
from os import listdir, path
from os.path import abspath, isfile

import numpy as np
from matplotlib import pyplot as plt

from read_files import read_collisions_with_obstacle, read_unique_collisions_with_obstacle


def group_by_first_element(zip_object):
    # Create a default dictionary to hold lists
    grouped = defaultdict(list)

    # Iterate through the zip object and group by the first element
    for first, second in zip_object:
        grouped[first].append(second)

    # Convert the defaultdict to a list of lists
    result = list(grouped.values())
    return result


def plot_observable(x_values, y_values, y_label, output):
    print(x_values)
    # Calculate means and standard deviations
    unique_x = np.unique(x_values)
    means = []
    std_devs = []

    for x in unique_x:
        # Get the corresponding y values for each unique x
        corresponding_y = [y for x_val, y in zip(x_values, y_values) if x_val == x]
        print('CORRESPONDING ' + str(corresponding_y))
        means.append(np.mean(corresponding_y))
        std_devs.append(np.std(corresponding_y))

    print(means)
    print(std_devs)

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(unique_x, means, yerr=std_devs, capsize=5, color='blue', alpha=0.7)
    plt.xlabel('Energía cinética (J)')
    plt.ylabel(y_label)
    plt.xticks(unique_x)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(output, dpi=400)
    plt.close()


def extract_velocity_from_filename(file_path):
    file_name = file_path.split('/')[-1]
    numbers = re.findall(r'\d+', file_name)
    return int(numbers[0]) if numbers else None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: plot_observable.py <output_file_pattern>")
        sys.exit(1)

    output_file = sys.argv[1]

    output_path = abspath(output_file)[:abspath(output_file).rfind('/')]

    start_time = time.time()

    files = [f for f in listdir(output_path) if
             isfile(path.join(output_path, f)) and 'collisions' in f]

    print(f"Output files: {files}")

    collisions_by_file = [read_collisions_with_obstacle(path.join(output_path, f)) for f in files]
    unique_collisions_by_file = [read_unique_collisions_with_obstacle(path.join(output_path, f)) for f in files]
    velocities_by_file = [extract_velocity_from_filename(path.join(output_path, f)) for f in files]
    print(collisions_by_file)
    print(unique_collisions_by_file)

    k_energies = [0.5 * 1 * (v ** 2) for v in velocities_by_file]

    plot_observable(k_energies, collisions_by_file, 'Colisiones totales con obstáculo', 'total_collisions_kinetic.png')
    plot_observable(k_energies, unique_collisions_by_file, 'Tiempo hasta que ½ de las partículas han colisionado (s)', 'new_collisions_kinetic.png')

    print(f"Elapsed time: {time.time() - start_time} s")