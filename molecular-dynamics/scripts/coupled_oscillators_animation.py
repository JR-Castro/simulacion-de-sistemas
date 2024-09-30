import math
import time

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation

N = 1000

def update_animation(frame, data, ax, dt, frames):
    print(f"Frame: {frame}/{frames}")
    ax.clear()

    ax.set_xlabel('N')
    ax.set_ylabel('y (m)')
    ax.set_ylim(-0.005, 0.005)
    ax.set_xlim(0, N)

    # Enhance background aesthetics
    ax.set_facecolor('#f0f0f0')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Calculate the current time for the given frame
    current_time = frame * dt

    # Filter the data for the current time, accounting for float error
    time_data = data.iloc[frame * N:(frame + 1) * N, :]
    # print(f"Slice: [{frame * 1000}: {(frame + 1) * 1000-1}], len: {len(time_data)}")
    if len(time_data) != N:
        print("Error")

    # Plot the oscillators' positions as blue dots
    ax.scatter(time_data.index % N, time_data['position'], c=time_data['position'], cmap='coolwarm', s=20,)

    # Display the current time with a semi-transparent background
    time_text = f"Time: {current_time:.2f}s"
    ax.text(0.5, 1.05, time_text, transform=ax.transAxes, fontsize=12,
            horizontalalignment='center', verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))


if __name__ == '__main__':
    start_time = time.time()
    data_coupled = pd.read_csv('coupled_oscillators.csv')
    data_coupled = data_coupled.iloc[N*500:, :]
    print(len(data_coupled))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    fps = 24
    dt = math.pow(10, -2)

    frames = int(len(data_coupled['time'])/N)
    # frames = 500

    ani = animation.FuncAnimation(fig, update_animation, frames=frames, fargs=(data_coupled, ax, dt, frames))

    ani.save('coupled_oscillators.mp4', fps=fps, dpi=300)
    plt.close(fig)

    print(f"Time taken: {time.time() - start_time:.2f}s")
