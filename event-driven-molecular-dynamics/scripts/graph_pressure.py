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

            p1_id, p1_x, p1_y, p1_vx, p1_vy = p1  # Obstacle
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


def graph_pressure(wall_pressures, obstacle_pressures, output_file):
    wall_times = [p['time'] for p in wall_pressures[0]]
    wall_data = [[p['pressure'] for p in pressure] for pressure in wall_pressures]

    obstacle_times = [p['time'] for p in obstacle_pressures[0]]
    obstacle_data = [[p['pressure'] for p in pressure] for pressure in obstacle_pressures]

    wall_np = np.array(wall_data)
    wall_mean = np.mean(wall_np, axis=0)
    wall_std = np.std(wall_np, axis=0)

    obstacle_np = np.array(obstacle_data)
    obstacle_mean = np.mean(obstacle_np, axis=0)
    obstacle_std = np.std(obstacle_np, axis=0)

    # Improve the y-axis scale by narrowing the limits to better visualize variations
    plt.plot(wall_times, wall_mean, linestyle='--', marker='o', color='blue', label='Pared')
    plt.plot(obstacle_times, obstacle_mean, linestyle='--', marker='o', color='red', label='Obstáculo')

    plt.fill_between(wall_times,
                     [a - s for a, s in zip(wall_mean, wall_std)],
                     [a + s for a, s in zip(wall_mean, wall_std)],
                     color='blue', alpha=0.2)
    plt.fill_between(obstacle_times,
                     [a - s for a, s in zip(obstacle_mean, obstacle_std)],
                     [a + s for a, s in zip(obstacle_mean, obstacle_std)],
                     color='red', alpha=0.2)

    plt.xlabel("Tiempo (s)", fontsize=12)
    plt.ylabel("Presión (N/m)", fontsize=12)

    # Set y-axis limits to make the fluctuations more visible
    # plt.ylim((min(avg) - max(std), max(avg) + max(std)))

    plt.grid(True, linestyle='--', alpha=0.6)
    # plt.title('Pressure over Time', fontsize=14)
    # Legend outside of graph
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True)
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
             isfile(path.join(output_path, f)) and re.match(output_file_pattern,
                                                            f) and 'collisions' in f and 'wall' not in f]

    print(f"Output files: {files}")

    collisions = [read_collisions(path.join(output_path, f)) for f in files]

    wall_pressures = [calculate_wall_pressures(static, c, 0.01) for c in collisions]
    print()
    obstacle_pressures = [calculate_obstacle_pressures(static, c, 0.1) for c in collisions]

    graph_pressure(wall_pressures, obstacle_pressures, "pressures.png")

    print(f"\nTotal time: {time.time() - start_time}s")
