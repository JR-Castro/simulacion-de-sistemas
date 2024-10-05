import math
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from generate_static import K_VALUES, RUNS, calculate_test_w_values, DEFAULT_K

N = 100
FONT = {'family': 'serif',
        'color': 'black',
        'weight': 'normal',
        'size': 14}
OUTPUT_DIR = 'amplitude'


def compute_square_error(c, x_values, real):
    predicted = [c * x for x in x_values]
    squared_errors = [(p - r) ** 2 for p, r in zip(predicted, real)]
    return sum(squared_errors)


def graph_amplitude_over_time(df, output_file, w):
    frames = int(len(df['time']) / N)
    amplitudes = [df.iloc[i * N:(i + 1) * N, :]['position'].max() for i in range(frames)]

    time = [df.iloc[i * N]['time'] for i in range(frames)]

    plt.plot(time, amplitudes)
    plt.xlabel('Tiempo (s)', fontdict=FONT)
    plt.ylabel('$A$ (m)', fontdict=FONT)
    plt.savefig(output_file, dpi=300)
    plt.clf()


if __name__ == '__main__':
    start_time = time.time()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    w_values = calculate_test_w_values(DEFAULT_K)

    runs = range(len(w_values))
    files = [f'output/coupled_oscillator_w{i}.csv' for i in runs]

    print("=== DEFAULT K ANALYSIS ===")
    amplitude = []
    for i, file in enumerate(files):
        df = pd.read_csv(file)

        amplitude.append(df['position'].max())

        print(f"w = {w_values[i]}, a = {amplitude[-1]}")

    plt.plot(w_values, amplitude, '.-')

    plt.xlabel('ω (rad/s)', fontdict=FONT)
    plt.ylabel('$A$ (m)', fontdict=FONT)

    plt.savefig(f'{OUTPUT_DIR}/amplitude_analysis.png', dpi=300)
    plt.clf()

    print("=== K ANALYSIS ===")

    files = [[f'output/coupled_oscillator_k{i}_{j}.csv' for j in range(RUNS)] for i in range(len(K_VALUES))]

    resonance_w = {}
    max_w_idx = {}

    for i, k in enumerate(K_VALUES):
        w_values = calculate_test_w_values(k)
        amplitudes = [pd.read_csv(file)['position'].max() for file in files[i]]
        max_w_idx[k] = amplitudes.index(max(amplitudes))
        resonance_w[k] = w_values[amplitudes.index(max(amplitudes))]
        for w, a in zip(w_values, amplitudes):
            print(f"k = {k}, w = {w}, a = {a}")
        plt.plot(calculate_test_w_values(k), amplitudes, '.--', label=f'k = {k}')

    plt.xlabel('ω (rad/s)', fontdict=FONT)
    plt.ylabel('$A$ (m)', fontdict=FONT)
    plt.legend()
    plt.savefig(f'{OUTPUT_DIR}/amplitude_analysis_k.png', dpi=300)
    plt.clf()

    for i, k in enumerate(resonance_w.keys()):
        graph_amplitude_over_time(pd.read_csv(files[i][max_w_idx[k]]), f'max_amplitude_time_k{i}.png', resonance_w[k])

    xs = [math.sqrt(k) for k in K_VALUES]
    ys = [resonance_w[k] for k in K_VALUES]
    plt.xlabel('$k^{1/2}$ (N/m)', fontdict=FONT)
    plt.ylabel('ω (rad/s)', fontdict=FONT)

    plt.scatter(xs, ys, marker='o', label="Resonancia", color='blue')

    numerator = sum(x * y for x, y in zip(xs, ys))
    denominator = sum(x ** 2 for x in xs)
    c_fit = numerator / denominator

    print(f"Best c: {c_fit} * x")
    print(f"Error: {compute_square_error(c_fit, xs, ys)}")

    plt.plot(xs, [c_fit * x for x in xs], linestyle='--',
             label=f'f(x) = {c_fit:.2f}x (ECM = {compute_square_error(c_fit, xs, ys):.3f})', color='red')
    plt.legend()

    plt.savefig(f'{OUTPUT_DIR}/resonance_analysis.png', dpi=300)
    plt.clf()

    c_values = np.linspace(c_fit - 0.15, c_fit + 0.15, 250)

    errors = [compute_square_error(c, xs, ys) for c in c_values]
    min_error_idx = errors.index(min(errors))

    plt.plot(c_values, errors, label="Error cuadrático", color='blue')
    plt.plot(c_values[min_error_idx], min(errors), linestyle='', marker='o', color='black', label=f"Mejor c")

    plt.axvline(x=c_fit, color='grey', linestyle='--')
    plt.axhline(y=min(errors), color='grey', linestyle='--')

    plt.xlabel('c', fontdict=FONT)
    plt.ylabel('Error cuadrático medio', fontdict=FONT)

    plt.legend(loc='upper right')
    plt.savefig(f'{OUTPUT_DIR}/resonance_error_analysis.png', dpi=300)

    print(f"Execution time: {time.time() - start_time:.2f}s")
