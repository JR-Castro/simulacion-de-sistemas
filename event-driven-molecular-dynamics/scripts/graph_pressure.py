import math
import re
import sys
from os import listdir, path
from os.path import abspath, isfile
import matplotlib.pyplot as plt

from read_files import read_collisions, read_static_file


def calculate_obstacle_pressures(static, collisions, dt):
    collisions = [c for c in collisions if 1 in [p[0] for p in c['particles']]]
    obstacle_radius = static['particles'][0][1]
    pressures = []

    for c in collisions:
        p1 = c['particles'][0]
        p2 = c['particles'][1]
        if p2[0] == 1:
            # p2 is the obstacle
            p1 = p2
            p2 = c['particles'][0]

        diff_x = p1[1] - p2[1]
        diff_y = p1[2] - p2[2]
        dist = math.sqrt(diff_x ** 2 + diff_y ** 2)
        n_x = diff_x / dist
        n_y = diff_y / dist

        v_n = p2[3] * n_x + p2[4] * n_y

        p_mass = static['particles'][p2[0]-1][2]
        p_radius = static['particles'][p2[0]-1][1]


        pressures.append({
            'time': c['time'],
            'pressure': 2 * p_mass * v_n * v_n / (p_radius * 2 * math.pi * obstacle_radius)
        })

    steps = int(static['time'] / dt)

    output = []
    for step in range(1, steps):
        s_time = step * dt

        s_pressures = [p['pressure'] for p in pressures if p['time'] <= s_time < p['time'] + dt]
        output.append({
            'time': s_time,
            'pressure': sum(s_pressures)
        })

    return output

def calculate_wall_pressures(static, collisions, dt):
    collisions = [c for c in collisions if len(c['particles']) == 1]

    radius = static['length'] / 2
    pressures = []
    for c in collisions:
        # Calculate normal vector
        p = c['particles'][0]
        p_info = static['particles'][p[0] - 1]
        n_x = -p[1] / (radius - p_info[1])
        n_y = -p[2] / (radius - p_info[1])

        v_n = p[3] * n_x + p[4] * n_y

        # Calculate momentum from collision, P = 2*m*v_n
        # momentum = 2 * p_info[2] * v_n (kg*m/s)
        # t_c = p_info[1] / v_n (s)
        # force = momentum / t_c (N)
        # force = 2 * p_info[2] * v_n * v_n / p_info[1]
        # pressure = force / (2 * pi * radius)
        pressures.append({
            'time': c['time'],
            'pressure': 2 * p_info[2] * v_n * v_n / (p_info[1] * 2 * math.pi * radius)
        })

    steps = int(static['time'] / dt)

    output = []
    for step in range(1, steps):
        s_time = step * dt

        s_pressures = [p['pressure'] for p in pressures if p['time'] <= s_time < p['time'] + dt]
        output.append({
            'time': s_time,
            'pressure': sum(s_pressures)
        })

    return output


def graph_pressure(pressures, output_file):
    times = [p['time'] for p in pressures[0]]
    data = [[p['pressure'] for p in pressure] for pressure in pressures]

    avg = [sum([d[i] for d in data]) / len(data) for i in range(len(data[0]))]
    std = [math.sqrt(sum([(d[i] - avg[i]) ** 2 for d in data]) / len(data)) for i in range(len(data[0]))]

    # Improve the y-axis scale by narrowing the limits to better visualize variations
    plt.plot(times, avg, linestyle='--', marker='.', color='blue')

    plt.fill_between(times,
                     [a - s for a, s in zip(avg, std)],
                     [a + s for a, s in zip(avg, std)],
                     color='blue', alpha=0.2)

    plt.xlabel("Tiempo (s)", fontsize=12)
    plt.ylabel("Presión (Pa)", fontsize=12)

    # Set y-axis limits to make the fluctuations more visible
    plt.ylim(bottom = 0.0)

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

    files = [f for f in listdir(output_path) if
             isfile(path.join(output_path, f)) and re.match(output_file_pattern, f) and 'collisions' in f]

    collisions = [read_collisions(path.join(output_path, f)) for f in files]

    wall_pressures = [calculate_wall_pressures(static, c, 0.1) for c in collisions]
    obstacle_pressures = [calculate_obstacle_pressures(static, c, 0.1) for c in collisions]

    graph_pressure(wall_pressures, "wall_pressure.png")
    graph_pressure(obstacle_pressures, "obstacle_pressure.png")
