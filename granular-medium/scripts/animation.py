import time

import numpy as np
import pandas as pd
from matplotlib import animation
import matplotlib.pyplot as plt

N = 100
W = 0.2
L = 0.7
OBSTACLE_RADIUS = 0.01
PARTICLE_RADIUS = 0.01

cm_to_points = lambda cm: (cm / 2.54) * 72

OBSTACLE_SIZE = cm_to_points(OBSTACLE_RADIUS)
PARTICLE_SIZE = cm_to_points(PARTICLE_RADIUS)


def update_animation(frame, data, scatter, text, frames):
    print(f"\rFrame: {frame}/{frames}", end='')

    # Filter the data for the current time
    time_data = data.iloc[frame * N:(frame + 1) * N, :]

    if len(time_data) != N:
        print("Error")

    # Plot the oscillators' positions as blue dots
    data = np.stack([time_data['x'], time_data['y']]).T
    scatter.set_offsets(data)

    # Display the current time with a semi-transparent background
    text.set_text(f"Time: {time_data['time'].iloc[0]:.2f}s")

    return scatter, text

if __name__ == '__main__':
    start_time = time.time()
    obstacles = pd.read_csv("outputObstacles.csv")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_ylim(0, W)
    ax.set_xlim(0, L)

    obstacleSctr = ax.scatter(
        obstacles['x'],
        obstacles['y'],
        s=OBSTACLE_SIZE,
        color='black'
    )

    data = pd.read_csv("outputStates.csv")

    particleSctr = ax.scatter(
        data.iloc[0:N, :]['x'],
        data.iloc[0:N, :]['y'],
        s=PARTICLE_SIZE,
        color='blue'
    )

    time_text = f"Time: {data['time'].iloc[0]:.2f}s"
    text = ax.text(0.5, 1.05, time_text, transform=ax.transAxes, fontsize=12,
                   horizontalalignment='center', verticalalignment='top',
                   bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    frames = int(len(data['time']) / N)
    # frames = 1000

    ani = animation.FuncAnimation(
        fig,
        update_animation,
        frames=frames,
        fargs=(data, particleSctr, text, frames)
    )
    ani.save("particles.mp4", fps=24, dpi=300)
    plt.close(fig)

    print(f"\rTime taken: {time.time() - start_time:.2f}s")