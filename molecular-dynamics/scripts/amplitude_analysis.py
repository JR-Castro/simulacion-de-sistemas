import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from generate_static import K_VALUES, RUNS, calculate_test_w_values, DEFAULT_K, get_dt
from graph_constants import DPI, FONT, COLOR_PALETTE, formatter

N = 100
OUTPUT_DIR = 'amplitude'


def compute_square_error(c, x_values, real):
    predicted = [x ** c for x in x_values]
    squared_errors = [(p - r) ** 2 for p, r in zip(predicted, real)]
    return sum(squared_errors)


def graph_amplitude_over_time(df, output_file, w, k):
    fig, ax = plt.subplots(figsize=(10, 6))
    frames = int(len(df['time']) / N)
    amplitudes = [df.iloc[i * N:(i + 1) * N, :]['position'].max() for i in range(frames)]

    time = [df.iloc[i * N]['time'] for i in range(frames)]

    plt.plot(time, amplitudes, color=COLOR_PALETTE[0])
    plt.xlabel('Tiempo (s)', fontdict=FONT)
    plt.ylabel('$A$ (m)', fontdict=FONT)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.subplots_adjust(right=0.75)
    plt.text(1.05, 0.5,
             f'$k$ = {k}\n'
             f'$ω$ = {w}\n'
             f'$dt_1$ = {formatter(get_dt(w), None)}\n'
             , fontdict=FONT, ha='left', va='center', transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(output_file, dpi=DPI)
    plt.clf()


def graph_amplitude_default(w_values, runs, output, k):
    files = [f'output/coupled_oscillator_w{i}.csv' for i in runs]

    amplitude = []
    for i, file in enumerate(files):
        df = pd.read_csv(file)

        amplitude.append(df['position'].max())

        print(f"w = {w_values[i]}, a = {amplitude[-1]}")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(w_values, amplitude, '.-', color=COLOR_PALETTE[1])

    plt.xlabel('ω (rad/s)', fontdict=FONT)
    plt.ylabel('$A$ (m)', fontdict=FONT)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)

    plt.subplots_adjust(right=0.75)
    plt.text(1.05, 0.5,
             f'$k$ = {k}\n'
             , fontdict=FONT, ha='left', va='center', transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(output, dpi=DPI)
    plt.clf()


def graph_amplitude_k(output):
    files = [[f'output/coupled_oscillator_k{i}_{j}.csv' for j in range(RUNS)] for i in range(len(K_VALUES))]

    resonance_w = {}
    max_w_idx = {}

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, k in enumerate(K_VALUES):
        w_values = calculate_test_w_values(k)
        amplitudes = [pd.read_csv(file)['position'].max() for file in files[i]]
        max_w_idx[k] = amplitudes.index(max(amplitudes))
        resonance_w[k] = w_values[amplitudes.index(max(amplitudes))]
        for w, a in zip(w_values, amplitudes):
            print(f"k = {k}, w = {w}, a = {a}")
        plt.plot(calculate_test_w_values(k), amplitudes, '.--', label=f'k = {k}',
                 color=COLOR_PALETTE[i % len(COLOR_PALETTE)])

    # plt.subplots_adjust(right=0.75)
    # plt.text(1.05, 0.5, f''
    #             , fontdict=FONT, ha='left', va='center', transform=ax.transAxes)
    plt.xlabel('ω (rad/s)', fontdict=FONT)
    plt.ylabel('$A$ (m)', fontdict=FONT)
    plt.yscale('log')

    current_ticks = ax.get_xticks()
    ticks = sorted({current_ticks[0], current_ticks[-1]}.union(list(resonance_w.values())))
    plt.xticks(ticks, labels=[f'{w:.2f}' for w in ticks], fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc='upper left')
    plt.savefig(output, dpi=DPI)
    plt.clf()

    return resonance_w, max_w_idx


def graph_w_vs_k(resonance_w, max_w_idx):
    files = [[f'output/coupled_oscillator_k{i}_{j}.csv' for j in range(RUNS)] for i in range(len(K_VALUES))]

    for i, k in enumerate(resonance_w.keys()):
        graph_amplitude_over_time(pd.read_csv(files[i][max_w_idx[k]]), f'max_amplitude_time_k{i}.png', resonance_w[k],
                                  k)

    xs = K_VALUES
    ys = [resonance_w[k] for k in K_VALUES]

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.xlabel('$k$ (N/m)', fontdict=FONT)
    plt.ylabel('ω (rad/s)', fontdict=FONT)

    plt.scatter(xs, ys, marker='o', label="Resonancia")

    c_values = np.linspace(0.5 - 0.5, 0.5 + 0.5, 500)
    errors = [compute_square_error(c, xs, ys) for c in c_values]
    min_error_idx = errors.index(min(errors))
    c_fit = float(c_values[min_error_idx])

    print(f"Best c: {c_fit} * x")
    print(f"Error: {compute_square_error(c_fit, xs, ys)}")

    plt.plot(xs, [x ** c_fit for x in xs], linestyle='--',
             label=f'f(x) = $x^{{{c_fit:.2f}}}$ (ECM = {errors[min_error_idx]:.2f})',
             color=COLOR_PALETTE[1])
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f'{OUTPUT_DIR}/resonance_analysis.png', dpi=DPI)
    plt.clf()


    plt.plot(c_values, errors, label="Error cuadrático", color='blue')
    plt.plot(c_values[min_error_idx], min(errors), linestyle='', marker='o', color='black', label=f"Mejor c")

    plt.axvline(x=c_fit, color='grey', linestyle='--')
    plt.axhline(y=min(errors), color='grey', linestyle='--')

    plt.xlabel('c', fontdict=FONT)
    plt.ylabel('Error cuadrático medio', fontdict=FONT)

    plt.legend(loc='upper right')
    plt.savefig(f'{OUTPUT_DIR}/resonance_error_analysis.png', dpi=DPI)


if __name__ == '__main__':
    start_time = time.time()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    w_values = calculate_test_w_values(DEFAULT_K)

    runs = range(len(w_values))

    print("=== DEFAULT K ANALYSIS ===")
    graph_amplitude_default(w_values, runs, f'{OUTPUT_DIR}/amplitude_analysis.png', DEFAULT_K)

    print("=== K ANALYSIS ===")
    resonance_w, max_w_idx = graph_amplitude_k(f'{OUTPUT_DIR}/amplitude_analysis_k.png')

    graph_w_vs_k(resonance_w, max_w_idx)

    print(f"Execution time: {time.time() - start_time:.2f}s")
