import time

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation

N = 100
M = 100
W = 20
L = 70
OBSTACLE_RADIUS = 0.5
PARTICLE_RADIUS = 0.5

DPI = 100

def update_animation(frame, data, particles, text, frames):
    print(f"Frame: {frame}/{frames}", end='\r')

    # Filter the data for the current time
    time_data = data.iloc[frame * N:(frame + 1) * N, :]

    if len(time_data) != N:
        print("Error")

    # Plot the oscillators' positions as blue dots
    # data = np.stack([time_data['x'], time_data['y']]).T
    # scatter.set_offsets(data)

    for i in range(N):
        particles[i].center = (time_data['x'].iloc[i], time_data['y'].iloc[i])

    # Display the current time with a semi-transparent background
    text.set_text(f"Time: {time_data['time'].iloc[0]:.2f}s")

    return particles, text

if __name__ == '__main__':
    start_time = time.time()
    obstacles = pd.read_csv("outputs/1_0_obstacles.csv")
    data = pd.read_csv("outputs/1_0_states.csv")

    # Convert centimeters to inches for matplotlib
    fig_width_inch = L / 2.54
    fig_height_inch = W / 2.54

    fig,ax = plt.subplots(figsize=(fig_width_inch, fig_height_inch), dpi=DPI)

    ax.set_xlabel('x (cm)')
    ax.set_ylabel('y (cm)')
    ax.set_ylim(0, W)
    ax.set_xlim(0, L)
    ax.set_aspect('equal')

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
        fargs=(data, particles, text, frames)
    )
    ani.save("particles.mp4", fps=24, dpi=100)
    plt.close(fig)

    print(f"\rTime taken: {time.time() - start_time:.2f}s")