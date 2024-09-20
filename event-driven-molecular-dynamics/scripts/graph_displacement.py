import math
import sys

import matplotlib.pyplot as plt
import numpy as np

from read_files import read_collisions, read_static_file

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: graph_displacement.py <static_file> <output_file> <collisions_file> [collisions_files...]")
        sys.exit(1)

    static_file = sys.argv[1]
    output_file = sys.argv[2]
    collisions_files = sys.argv[3:]

    static = read_static_file(static_file)

    times = [step * static["time"] / 100.0 for step in range(100)]
    all_displacements = []

    for i, collisions_file in enumerate(collisions_files):
        print("{:.0f}%".format(i * 100 / len(collisions_files)))
        collisions = read_collisions(collisions_file)

        is_obstacle_collision = lambda particles: particles[0][0] == 1 or (len(particles) == 2 and particles[1][0] == 1)
        get_obstacle_position = lambda particles: particles[0][1:3] if particles[0][0] == 1 else particles[1][1:3]

        obstacle_states = [
            [collision["time"], get_obstacle_position(collision["particles"])]
            for collision in collisions
            if is_obstacle_collision(collision["particles"])
        ]

        positions = [next((state[1] for state in obstacle_states if state[0] > time)) for time in times]
        displacements = [math.sqrt(position[0] ** 2 + position[1] ** 2) for position in positions]

        all_displacements.append(displacements)

    data = np.vstack(all_displacements)
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0, ddof=1)

    plt.xlim(0, static["time"])
    plt.errorbar(times, mean, std, marker='.')
    plt.xlabel("Tiempo (s)", fontsize=12)
    plt.ylabel("Desplazamiento cuadrático medio", fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(output_file, dpi=400)
