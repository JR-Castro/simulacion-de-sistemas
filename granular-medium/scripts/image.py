import time

import matplotlib.pyplot as plt
import pandas as pd

from animation import W, L, N, PARTICLE_RADIUS, M

if __name__ == '__main__':
    start_time = time.time()
    obstacles = pd.read_csv("outputObstacles.csv")
    data = pd.read_csv("outputStates.csv")

    fig_dpi = 100  # resolution

    # Convert centimeters to inches for matplotlib
    fig_width_inch = L / 2.54
    fig_height_inch = W / 2.54

    # Set up the figure
    fig, ax = plt.subplots(figsize=(fig_width_inch, fig_height_inch), dpi=fig_dpi)

    # Draw the container boundaries
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)

    # Add the circle to represent the particle
    obstacles = [
        plt.Circle((obstacles['x'][i], obstacles['y'][i]), PARTICLE_RADIUS, color="black") for i in range(M)
    ]
    for obstacle in obstacles:
        ax.add_patch(obstacle)

    particles = [
        plt.Circle((data['x'][i], data['y'][i]), PARTICLE_RADIUS, color="blue") for i in range(N)
    ]
    for particle in particles:
        ax.add_patch(particle)

    # Customize plot
    ax.set_aspect('equal')
    ax.set_xlabel("Width (cm)")
    ax.set_ylabel("Height (cm)")
    ax.set_title("Particle in Container")

    plt.show()
    print(f"\rTime taken: {time.time() - start_time:.2f}s")
