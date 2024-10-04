import time

import matplotlib.pyplot as plt
import pandas as pd

from generate_static import K_VALUES, RUNS, calculate_test_w_values, DEFAULT_K

N = 100
FONT = {'family': 'serif',
        'color': 'black',
        'weight': 'normal',
        'size': 14}

if __name__ == '__main__':
    start_time = time.time()

    w_values = calculate_test_w_values(DEFAULT_K)

    runs = range(len(w_values))
    files = [f'output/coupled_oscillator_w{i}.csv' for i in runs]

    amplitude = []
    for i, file in enumerate(files):
        df = pd.read_csv(file)

        if i == runs[0] or i == runs[int(len(runs) / 2)]:
            frames = int(len(df['time']) / N)
            amplitudes = [df.iloc[i * N:(i + 1) * N, :]['position'].max() for i in range(frames)]

            plt.plot(range(frames), amplitudes)
            plt.xlabel('Frame', fontdict=FONT)
            plt.ylabel('Amplitude (m)', fontdict=FONT)
            plt.savefig(f'amplitude_analysis_{i}.png', dpi=300)
            plt.clf()

        amplitude.append(df['position'].max())

    plt.plot(w_values, amplitude, '.-')

    plt.xlabel('w (rad/s)', fontdict=FONT)
    plt.ylabel('Amplitude (m)', fontdict=FONT)

    plt.savefig('amplitude_analysis.png', dpi=300)
    plt.clf()

    files = [[f'output/coupled_oscillator_k{i}_{j}.csv' for j in range(RUNS)] for i in range(len(K_VALUES))]

    for i, k in enumerate(K_VALUES):
        amplitudes = [pd.read_csv(file)['position'].max() for file in files[i]]
        plt.plot(calculate_test_w_values(k), amplitudes, '.--', label=f'k = {k}')

    plt.xlabel('w (rad/s)', fontdict=FONT)
    plt.ylabel('Amplitude (m)', fontdict=FONT)
    plt.legend()
    plt.savefig('amplitude_analysis_k.png', dpi=300)

    print(f"Execution time: {time.time() - start_time:.2f}s")
