import json
import os
import random

from animation import OBSTACLE_RADIUS, L, PARTICLE_RADIUS, W

RUNS = 5

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
        "a0": 1,
        "time": 100.0,
        "N": 100,
        "M": 100,
        "dt": 1E-3,
        "dt2Interval": 10, # Print every 1E-2 seconds
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
