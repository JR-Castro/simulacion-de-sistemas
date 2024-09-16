import re
import sys
import time
from os import path, listdir
from os.path import abspath, isfile

import matplotlib.pyplot as plt
import numpy as np

from read_files import read_static_file, read_states_output_file


def calculate_kinetic(static, states):
    kinetics = []

    for s in states:
        kinetic = 0
        for p in s['particles']:
            p_info = static['particles'][p[0] - 1]
            if p_info[2] == float('inf'):
                continue
            kinetic += 0.5 * p_info[2] * (p[3] ** 2 + p[4] ** 2)

        kinetics.append({'time': s['time'], 'kinetic': kinetic})

    return kinetics


def graph_kinetic(kinetics, output):
    times = [k['time'] for k in kinetics[0]]
    kinetic = [[k['kinetic'] for k in ks] for ks in kinetics]

    np_data = np.array(kinetic)
    avg = np.mean(np_data, axis=0)
    std = np.std(np_data, axis=0)

    plt.plot(times, avg, linestyle='--', marker='.', color='blue')

    plt.fill_between(times,
                        [avg[i] - std[i] for i in range(len(avg))],
                        [avg[i] + std[i] for i in range(len(avg))],
                        color='blue', alpha=0.2)

    plt.xlabel("Tiempo (s)", fontsize=12)
    plt.ylabel("Energía cinética (J)", fontsize=12)

    print(f"Min kinetic: {min(avg)}")
    print(f"Max kinetic: {max(avg)}")
    print(f"Min std: {min(std)}")
    print(f"Max std: {max(std)}")

    # plt.ylim(bottom=0.0)
    plt.ylim((0, max(avg) + max(std)))

    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    plt.savefig(output, dpi=400)
    plt.clf()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: run_simulations.py <static_file> <output_file_pattern>")
        sys.exit(1)

    static_file = sys.argv[1]
    output_file = sys.argv[2]

    static = read_static_file(static_file)
    output_path = abspath(output_file)[:abspath(output_file).rfind('/')]
    output_file_pattern = output_file[output_file.rfind('/') + 1:]

    start_time = time.time()

    files = [f for f in listdir(output_path) if
             isfile(path.join(output_path, f)) and re.match(output_file_pattern, f) and 'states' in f]

    print(f"Output files: {files}")

    states = [read_states_output_file(static, path.join(output_path, f)) for f in files]

    k_energies = [calculate_kinetic(static, s) for s in states]

    graph_kinetic(k_energies, 'kinetic.png')

    print(f"Elapsed time: {time.time() - start_time} s")
