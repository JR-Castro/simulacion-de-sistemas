import math
import re
import sys
import time
from os import listdir, path
from os.path import abspath, isfile
import matplotlib.pyplot as plt
import numpy as np

from read_files import read_collisions, read_static_file


def calculate_obstacle_pressures(static, collisions, dt):
    collisions = [c for c in collisions if 1 in [p[0] for p in c['particles']]]
    obstacle_radius = static['particles'][0][1]

    steps = int(static['time'] / dt)

    output = []
    minimum_collisions = 10E10
    for step in range(1, steps):
        s_time = step * dt

        filtered_collisions = [c for c in collisions if s_time - dt / 2 <= c['time'] < s_time + dt / 2]
        minimum_collisions = min(minimum_collisions, len(filtered_collisions))
        momentum = 0.0
        # Sum(M, 2Vn_i) / ( M * dt * 2 * pi * r), donde M es la cantidad de colisiones
        for c in filtered_collisions:
            p1 = c['particles'][0]
            p2 = c['particles'][1]
            if p2[0] == 1:
                # p2 is the obstacle
                p1 = p2
                p2 = c['particles'][0]

            p1_id, p1_x, p1_y, p1_vx, p1_vy = p1 # Obstacle
            p2_id, p2_x, p2_y, p2_vx, p2_vy = p2
            _, p2_r, p2_m = static['particles'][p2[0] - 1]

            diff_x = p2_x - p1_x
            diff_y = p2_y - p1_y
            dist = p2_r + obstacle_radius

            n_x = diff_x / dist
            n_y = diff_y / dist

            v_n = p2_vx * n_x + p2_vy * n_y

            momentum -= 2 * v_n * p2_m

        output.append({
            'time': s_time,
            'pressure': momentum / (len(filtered_collisions) * dt * 2 * math.pi * obstacle_radius)
        })

    print(f"Minimum collisions: {minimum_collisions}")
    return output


def calculate_wall_pressures(static, collisions, dt):
    collisions = [c for c in collisions if len(c['particles']) == 1]

    radius = static['length'] / 2

    steps = int(static['time'] / dt)

    output = []
    # max int
    minimum_collisions = 10E10
    for step in range(1, steps):
        s_time = step * dt

        filtered_collisions = [c for c in collisions if s_time - dt / 2 <= c['time'] < s_time + dt / 2]
        minimum_collisions = min(minimum_collisions, len(filtered_collisions))
        momentum = 0.0
        for c in filtered_collisions:
            p_id, p_x, p_y, p_vx, p_vy = c['particles'][0]
            _, p_r, p_m = static['particles'][p_id - 1]
            n_x = -p_x / (radius - p_r)
            n_y = -p_y / (radius - p_r)

            v_n = p_vx * n_x + p_vy * n_y

            momentum -= 2 * v_n * p_m

        output.append({
            'time': s_time,
            'pressure': momentum / (len(filtered_collisions) * dt * 2 * math.pi * radius)
        })

    print(f"Minimum collisions: {minimum_collisions}")
    return output


def graph_pressure(pressures, output_file):
    times = [p['time'] for p in pressures[0]]
    data = [[p['pressure'] for p in pressure] for pressure in pressures]

    np_data = np.array(data)
    avg = np.mean(np_data, axis=0)
    std = np.std(np_data, axis=0)

    # Improve the y-axis scale by narrowing the limits to better visualize variations
    plt.plot(times, avg, linestyle='--', marker='o', color='blue')

    plt.fill_between(times,
                     [a - s for a, s in zip(avg, std)],
                     [a + s for a, s in zip(avg, std)],
                     color='blue', alpha=0.2)

    plt.xlabel("Tiempo (s)", fontsize=12)
    plt.ylabel("Presión (N/m)", fontsize=12)

    # Set y-axis limits to make the fluctuations more visible
    # plt.ylim((min(avg) - max(std), max(avg) + max(std)))

    plt.grid(True, linestyle='--', alpha=0.6)
    # plt.title('Pressure over Time', fontsize=14)
    # plt.legend(loc='upper right')
    plt.tight_layout()

    plt.savefig(output_file, dpi=400)
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
             isfile(path.join(output_path, f)) and re.match(output_file_pattern, f) and 'collisions' in f and 'wall' not in f]

    print(f"Output files: {files}")

    collisions = [read_collisions(path.join(output_path, f)) for f in files]

    wall_pressures = [calculate_wall_pressures(static, c, 0.1) for c in collisions]
    print()
    obstacle_pressures = [calculate_obstacle_pressures(static, c, 0.1) for c in collisions]

    graph_pressure(wall_pressures, "wall_pressure.png")
    graph_pressure(obstacle_pressures, "obstacle_pressure.png")

    print(f"Total time: {time.time() - start_time}s")
