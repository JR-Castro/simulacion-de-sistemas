import math
import time

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation

N = 100
L0 = 1E-3
POSITIONS = [i * L0 for i in range(N)]
MAX_POSITION = max(POSITIONS)

def update_animation(frame, data, ax, dt, frames, amplitude):
    print(f"\rFrame: {frame}/{frames}", end='')
    ax.clear()

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_ylim(-amplitude, amplitude)
    ax.set_xlim(0, MAX_POSITION)

    # Enhance background aesthetics
    ax.set_facecolor('#f0f0f0')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Calculate the current time for the given frame

    # Filter the data for the current time, accounting for float error
    time_data = data.iloc[frame * N:(frame + 1) * N, :]
    # print(f"Slice: [{frame * 1000}: {(frame + 1) * 1000-1}], len: {len(time_data)}")
    if len(time_data) != N:
        print("Error")

    # Plot the oscillators' positions as blue dots
    ax.scatter(POSITIONS, time_data['position'], s=20,)

    # Display the current time with a semi-transparent background
    time_text = f"Time: {time_data['time'].iloc[0]:.2f}s"
    ax.text(0.5, 1.05, time_text, transform=ax.transAxes, fontsize=12,
            horizontalalignment='center', verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))


if __name__ == '__main__':
    start_time = time.time()
    data_coupled = pd.read_csv('output/coupled_oscillator_w10.csv')
    amplitude = max(data_coupled['position'].max(), abs(data_coupled['position'].min()))
    amplitude = round(amplitude, 2)
    # data_coupled = data_coupled.iloc[N*500:, :]
    print(len(data_coupled))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    fps = 20
    dt = math.pow(10, -2)

    frames = int(len(data_coupled['time'])/N)
    # frames = 1000

    ani = animation.FuncAnimation(fig, update_animation, frames=frames, fargs=(data_coupled, ax, dt, frames, amplitude))

    ani.save('coupled_oscillators.mp4', fps=fps, dpi=300)
    plt.close(fig)

    print(f"\rTime taken: {time.time() - start_time:.2f}s")
