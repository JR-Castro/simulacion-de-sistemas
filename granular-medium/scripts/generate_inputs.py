import json
import os
import random

import numpy as np

from animation import OBSTACLE_RADIUS, L, PARTICLE_RADIUS, W

DEFAULT_A0 = 1
DEFAULT_TIME = 600.0
DEFAULT_N = 100
DEFAULT_M = 100
DEFAULT_DT = 1E-3
DEFAULT_DT2_INTERVAL = 10

RUNS = 5

A0_VALUES = sorted([x for x in np.linspace(0.5, 5.0, 6)] + [DEFAULT_A0])

M_VALUES = [int(x) for x in np.linspace(80, 120, 5)]

def generate_obstacle_particles(M, N):
    # Generate obstacles
    obstacles = []

    for i in range(M):
        x = random.uniform(OBSTACLE_RADIUS, L - OBSTACLE_RADIUS)
        y = random.uniform(OBSTACLE_RADIUS, W - OBSTACLE_RADIUS)

        tries = 0
        while any((x - x1) ** 2 + (y - y1) ** 2 <= (2.0 * OBSTACLE_RADIUS) ** 2 for x1, y1 in obstacles):
            x = random.uniform(OBSTACLE_RADIUS, L - OBSTACLE_RADIUS)
            y = random.uniform(OBSTACLE_RADIUS, W - OBSTACLE_RADIUS)
            tries += 1

        print(tries)

        obstacles.append((x, y))

    print()
    # Generate particles
    particles = []
    for i in range(N):
        x = random.uniform(PARTICLE_RADIUS, L - PARTICLE_RADIUS)
        y = random.uniform(PARTICLE_RADIUS, W - PARTICLE_RADIUS)

        tries = 0
        while any((x - x1) ** 2 + (y - y1) ** 2 <= (OBSTACLE_RADIUS + PARTICLE_RADIUS) ** 2 for x1, y1 in obstacles) \
            or any((x - x1) ** 2 + (y - y1) ** 2 <= ( 2 * PARTICLE_RADIUS) ** 2 for x1, y1 in particles):
            x = random.uniform(OBSTACLE_RADIUS, L - OBSTACLE_RADIUS)
            y = random.uniform(OBSTACLE_RADIUS, W - OBSTACLE_RADIUS)
            tries += 1

        print(tries)

        particles.append((x, y))

    return obstacles, particles


if __name__ == '__main__':
    # Check if dir exists
    if not os.path.exists("inputs"):
        os.mkdir("inputs")

    if not os.path.exists("inputs/static"):
        os.mkdir("inputs/static")

    if not os.path.exists("inputs/dynamic"):
        os.mkdir("inputs/dynamic")

    if not os.path.exists("outputs"):
        os.mkdir("outputs")


    staticData = {
        "a0": DEFAULT_A0,
        "time": DEFAULT_TIME,
        "N": DEFAULT_N,
        "M": DEFAULT_M,
        "dt": DEFAULT_DT,
        "dt2Interval": DEFAULT_DT2_INTERVAL, # Print every 1E-2 seconds
    }

    with open(f"inputs/static/1.json", "w") as f:
        json.dump(staticData, f)

    for i in range(RUNS):
        obstacles, particles = generate_obstacle_particles(staticData["M"], staticData["N"])

        with open(f"inputs/dynamic/1_{i}.json", "w") as f:
            json.dump({
                "obstacles": obstacles,
                "particles": particles
            }, f)

    for i in range(len(A0_VALUES)):
        staticData["a0"] = A0_VALUES[i]
        with open(f"inputs/static/2_{i}.json", "w") as f:
            json.dump(staticData, f)

        for j in range(RUNS):
            obstacles, particles = generate_obstacle_particles(staticData["M"], staticData["N"])

            with open(f"inputs/dynamic/2_{i}_{j}.json", "w") as f:
                json.dump({
                    "obstacles": obstacles,
                    "particles": particles
                }, f)

    staticData["a0"] = DEFAULT_A0

    for i in range(len(M_VALUES)):
        staticData["M"] = M_VALUES[i]
        for j in range(len(A0_VALUES)):
            staticData["a0"] = A0_VALUES[j]

            with open(f"inputs/static/3_{i}_{j}.json", "w") as f:
                json.dump(staticData, f)

            for k in range(RUNS):
                obstacles, particles = generate_obstacle_particles(staticData["M"], staticData["N"])

                with open(f"inputs/dynamic/3_{i}_{j}_{k}.json", "w") as f:
                    json.dump({
                        "obstacles": obstacles,
                        "particles": particles
                    }, f)
