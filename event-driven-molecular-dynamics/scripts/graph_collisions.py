import re
import sys
import time
from os import listdir, path
from os.path import abspath, isfile

import matplotlib.pyplot as plt
import numpy as np

from read_files import read_static_file, read_collisions

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: run_simulations.py <static_file> <output_file_pattern>")
        sys.exit(1)

    static_file = sys.argv[1]
    output_files = sys.argv[2:]

    static = read_static_file(static_file)
    start_time = time.time()

    cum_avg_new_collisions = []
    cum_avg_total_collisions = []
    steps_array = []
    speeds = [3, 6, 10]

    for i, output_file in enumerate(output_files):
        output_path = abspath(output_file)[:abspath(output_file).rfind('/')]
        output_file_pattern = output_file[output_file.rfind('/') + 1:]

        files = [f for f in listdir(output_path) if
                 isfile(path.join(output_path, f)) and re.match(output_file_pattern, f) and 'collisions' in f]

        print(f"Output files: {files}")

        collisions = []
        for f in files:
            coll = read_collisions(path.join(output_path, f))
            collisions.append([c for c in coll if 1 in [p[0] for p in c['particles']]])

        dt = 0.1

        steps = range(0, int(static['time'] / dt))
        steps_array.append([s * dt for s in steps])

        total_collisions = np.zeros((len(collisions), len(steps)))
        new_collisions = np.zeros((len(collisions), len(steps)))

        prev_collided = [set() for _ in collisions]
        for step in steps:
            s_time = step * dt
            for i, coll in enumerate(collisions):
                filtered_collisions = [c for c in coll if c['time'] <= s_time < c['time'] + dt]
                total_collisions[i, step] = len(filtered_collisions)
                for c in filtered_collisions:
                    p1 = c['particles'][0]
                    p2 = c['particles'][1]
                    if p1[0] != 1 and p1[0] not in prev_collided[i]:
                        new_collisions[i, step] += 1
                        prev_collided[i].add(p1[0])
                    elif p2[0] != 1 and p2[0] not in prev_collided[i]:
                        new_collisions[i, step] += 1
                        prev_collided[i].add(p2[0])

        np.cumsum(new_collisions, axis=1, out=new_collisions)
        np.cumsum(total_collisions, axis=1, out=total_collisions)

        avg_new_collisions = np.mean(new_collisions, axis=0)
        cum_avg_new_collisions.append(avg_new_collisions)
        avg_total_collisions = np.mean(total_collisions, axis=0)
        cum_avg_total_collisions.append(avg_total_collisions)
        # std_new_collisions = np.std(new_collisions, axis=0)
        # std_total_collisions = np.std(total_collisions, axis=0)

    for i, avg_new_collisions in enumerate(cum_avg_new_collisions):
        steps = steps_array[i]
        plt.plot(steps, avg_new_collisions, linestyle='--', marker='o', label=f"$|v_0|$ = {speeds[i]} m/s")
        # plt.fill_between(steps,
        #                  [a - s for a, s in zip(avg_new_collisions, std_new_collisions)],
        #                  [a + s for a, s in zip(avg_new_collisions, std_new_collisions)],
        #                  color='blue', alpha=0.2)

    plt.xlabel("Tiempo (s)", fontsize=12)
    plt.ylabel("Colisiones nuevas con el obstáculo", fontsize=12)
    plt.legend(loc='upper left')

    plt.savefig('new_collisions.png', dpi=400)
    plt.clf()

    for i, avg_total_collisions in enumerate(cum_avg_total_collisions):
        steps = steps_array[i]
        plt.plot(steps, avg_total_collisions, linestyle='--', marker='o', label=f"$|v_0|$ = {speeds[i]} m/s")
        # plt.fill_between(steps,
        #                  [a - s for a, s in zip(avg_total_collisions, std_total_collisions)],
        #                  [a + s for a, s in zip(avg_total_collisions, std_total_collisions)],
        #                  color='blue', alpha=0.2)

    plt.xlabel("Tiempo (s)", fontsize=12)
    plt.ylabel("Colisiones totales con el obstáculo", fontsize=12)
    plt.legend(loc='upper left')

    plt.savefig('total_collisions.png', dpi=400)
    plt.clf()

    print(f"Execution time: {time.time() - start_time}")
