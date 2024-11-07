import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from generate_inputs import RUNS
from utils import compute_mean_square_error

if __name__ == '__main__':
    start_time = time.time()

    os.makedirs("analysis", exist_ok=True)

    with open("inputs/static/1.json") as f:
        static_data = json.load(f)

    dt = static_data["dt"]
    total_time = static_data['time']
    time_points = [i * dt for i in range(int(total_time / dt))]

    # Create an empty DataFrame to hold crossings data for each run
    runs_data = pd.DataFrame(index=time_points)
    for i in range(RUNS):
        # Read exit data and round exit times to the nearest multiple of dt for consistency
        exits = pd.read_csv(f"outputs/1_{i}_exits.csv")
        exits['time'] = (exits['time'] / dt).round() * dt

        # Use value_counts to get crossing counts at each time and reindex to fill missing times
        crossings_count = exits['time'].value_counts().reindex(time_points, fill_value=0)

        # Store cumulative crossings for this run in the DataFrame
        runs_data[f'run_{i}'] = crossings_count.cumsum()

    # Calculate average and standard deviation across all runs

    # runs_data['average'] = runs_data.mean(axis=1)
    # runs_data['std_dev'] = runs_data.std(axis=1)

    plt.figure(figsize=(10, 6))

    steady_states = []
    # y0s = []
    best_qs = []
    run_errors = []
    run_min_error_idx = []
    run_q_values = []
    run_x_values = []
    run_fit_x_values = []
    run_y0_values = []

    colors = ['blue', 'red', 'green', 'purple', 'orange', 'black', 'brown', 'pink', 'gray', 'cyan']

    xlim_error_min = 0.25
    xlim_error_max = 1.5
    ylim_error_min = 0.0
    # ylim_error_max = 0.0
    ylim_error_max = 50.0

    for i, run in enumerate(runs_data):
        print(f"Run {i}:")
        # print(runs_data)

        # First state where at least one particle crossed
        steady_state = 200.0
        steady_states.append(steady_state)

        # Obtain data after we reach a steady state
        filtered_data = runs_data[runs_data.index >= steady_state][run]

        # Fit a line to the data
        # y0 = filtered_data.iloc[0]
        # y0s.append(y0)
        x_values = filtered_data.index
        run_x_values.append(x_values)

        y_values = filtered_data
        y0 = y_values.iloc[0]
        run_y0_values.append(y0)

        q_values = np.linspace(0.0, 2.0, 200)
        run_q_values.append(q_values)

        fit_x_values = x_values - filtered_data.index[0]
        run_fit_x_values.append(fit_x_values)
        fit_y_values = y_values - y0

        errors = [compute_mean_square_error(q, fit_x_values, fit_y_values) for q in q_values]
        run_errors.append(errors)

        min_error_idx = errors.index(min(errors))
        run_min_error_idx.append(min_error_idx)

        # ylim_error_max = max(ylim_error_max, max(
        #     error for i, error in enumerate(errors) if xlim_error_min <= q_values[i] <= xlim_error_max))

        q_fit = float(q_values[min_error_idx])
        best_qs.append(q_fit)

        print(f"Best fit {i}: q = {q_fit}")
        print(f"Error {i}: {errors[min_error_idx]}")

        # Calculate the standard error
        # std_error = runs_data['std_dev'] / np.sqrt(RUNS)

        # Plotting
        plt.plot(runs_data.index, runs_data[run], label=i, color=colors[i])

        # plt.plot(x_values, [c_fit * x for x in x_values], linestyle='--',
        #          label=f'f(x) = {c_fit:.3f}x (ECM = {formatter(errors[min_error_idx], None)})', color=colors[i])

        # Fill between for standard error
        # plt.fill_between(
        #     runs_data.index,
        #     runs_data['average'] - std_error,
        #     runs_data['average'] + std_error,
        #     color="blue",
        #     alpha=0.2,
        #     label="Error"
        # )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Partículas")
    plt.legend(loc="upper left")
    plt.savefig("analysis/caudal.png", dpi=300)
    plt.clf()

    plt.figure(figsize=(10, 6))
    for i, run in enumerate(runs_data):
        plt.plot(runs_data.index, runs_data[run], alpha=0.5, color=colors[i])
        plt.plot(run_x_values[i],
                 [best_qs[i] * run_fit_x_values[i][j] + run_y0_values[i] for j in range(len(run_fit_x_values[i]))],
                 linestyle='--', color=colors[i],
                 label=f"Q = {best_qs[i]:.3f} $s^{-1}$ (ECM: {run_errors[i][run_min_error_idx[i]]:.3f})")

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Partículas")
    plt.legend(loc="upper left")
    plt.savefig("analysis/caudal_line_fits.png", dpi=300)
    plt.clf()

    plt.figure(figsize=(10, 6))
    # ax = plt.gca()
    # ax.yaxis.set_major_formatter(formatter)

    for i in range(RUNS):
        plt.plot(run_q_values[i], run_errors[i], label=i, color=colors[i])
        plt.plot(run_q_values[i][run_min_error_idx[i]], run_errors[i][run_min_error_idx[i]], linestyle='', marker='o',
                 # label=f"c = {best_cs[i]:.3f}",
                 color=colors[i])

    # plt.axvline(x=c_fit, color='grey', linestyle='--')
    # plt.axhline(y=min(errors), color='grey', linestyle='--')

    plt.xlim(xlim_error_min, xlim_error_max)
    plt.ylim(ylim_error_min, ylim_error_max)
    plt.xlabel('Q ($s^{-1}$)')
    plt.ylabel('ECM')

    plt.legend(loc='upper right')

    # print(filtered_data.index[0], filtered_data.iloc[0]['average'])
    # print(filtered_data.index[-1], filtered_data.iloc[-1]['average'])

    print(f"Execution time: {time.time() - start_time:.2f}s")
    plt.savefig("analysis/caudal_error.png", dpi=300)
