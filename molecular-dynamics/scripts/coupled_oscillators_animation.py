import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation

N = 100
L0 = 1E-3
POSITIONS = [i * L0 for i in range(N)]
MAX_POSITION = max(POSITIONS)


def update_animation(frame, data, scatter, text, frames):
    print(f"\rFrame: {frame}/{frames}", end='')

    # Filter the data for the current time
    time_data = data.iloc[frame * N:(frame + 1) * N, :]
    # print(f"Slice: [{frame * 1000}: {(frame + 1) * 1000-1}], len: {len(time_data)}")
    if len(time_data) != N:
        print("Error")

    # Plot the oscillators' positions as blue dots
    data = np.stack([POSITIONS, time_data['position']]).T
    scatter.set_offsets(data)

    # Display the current time with a semi-transparent background
    text.set_text(f"Time: {time_data['time'].iloc[0]:.2f}s")

    return scatter, text

if __name__ == '__main__':
    start_time = time.time()
    files = ['output/coupled_oscillator_anim_0.csv', 'output/coupled_oscillator_anim_1.csv']
    fps = [24, 120]
    for i, file in enumerate(files):
        data = pd.read_csv(file)
        amplitude = max(data['position'].max(), abs(data['position'].min()))
        amplitude = round(amplitude, 2)
        # data_coupled = data_coupled.iloc[N*500:, :]
        print(len(data))

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_ylim(-amplitude, amplitude)
        ax.set_xlim(0, MAX_POSITION)

        # Enhance background aesthetics
        ax.set_facecolor('#f0f0f0')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        scatter = ax.scatter(POSITIONS, data.iloc[0:N, :]['position'], s=20)

        time_text = f"Time: {data['time'].iloc[0]:.2f}s"
        text = ax.text(0.5, 1.05, time_text, transform=ax.transAxes, fontsize=12,
                       horizontalalignment='center', verticalalignment='top',
                       bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        frames = int(len(data['time']) / N)
        # frames = 500

        ani = animation.FuncAnimation(fig, update_animation, frames=frames, fargs=(data, scatter, text, frames))

        ani.save(f'coupled_oscillators_{i}.mp4', fps=fps[i], dpi=300)
        plt.close(fig)
        print()

    print(f"\rTime taken: {time.time() - start_time:.2f}s")
