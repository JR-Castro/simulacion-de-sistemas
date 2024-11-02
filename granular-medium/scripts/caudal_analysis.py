import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from generate_inputs import RUNS
from utils import formatter


def compute_square_error(c, x_values, real):
    predicted = [c * x for x in x_values]
    squared_errors = [(p - r) ** 2 for p, r in zip(predicted, real)]
    return sum(squared_errors)


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
    best_cs = []
    run_errors = []
    run_min_error_idx = []
    run_c_values = []
    run_x_values = []

    colors = ['blue', 'red', 'green', 'purple', 'orange', 'black', 'brown', 'pink', 'gray', 'cyan']

    for i, run in enumerate(runs_data):
        print(f"Run {i}:")
        # print(runs_data)

        # First state where at least one particle crossed
        steady_state = runs_data[runs_data[run] > 0].index[0]
        steady_states.append(steady_state)

        # Obtain data after we reach a steady state
        filtered_data = runs_data[runs_data.index >= steady_state][run]

        # Fit a line to the data
        x_values = filtered_data.index
        run_x_values.append(x_values)

        y_values = filtered_data

        c_values = np.linspace(0.0, 2.0, 400)
        run_c_values.append(c_values)

        errors = [compute_square_error(c, x_values, y_values) for c in c_values]
        run_errors.append(errors)

        min_error_idx = errors.index(min(errors))
        run_min_error_idx.append(min_error_idx)

        c_fit = float(c_values[min_error_idx])
        best_cs.append(c_fit)

        print(f"Best fit {i}: c = {c_fit}")
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
        plt.plot(run_x_values[i], [best_cs[i] * x for x in run_x_values[i]], linestyle='--', color=colors[i],
                 label=f"c = {best_cs[i]:.3f} (ECM: {formatter(run_errors[i][run_min_error_idx[i]], None)})")

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Partículas")
    plt.legend(loc="upper left")
    plt.savefig("analysis/caudal_line_fits.png", dpi=300)
    plt.clf()

    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.yaxis.set_major_formatter(formatter)

    for i in range(RUNS):
        plt.plot(run_c_values[i], run_errors[i], label=i, color=colors[i])
        plt.plot(run_c_values[i][run_min_error_idx[i]], run_errors[i][run_min_error_idx[i]], linestyle='', marker='o',
                 # label=f"c = {best_cs[i]:.3f}",
                 color=colors[i])

    # plt.axvline(x=c_fit, color='grey', linestyle='--')
    # plt.axhline(y=min(errors), color='grey', linestyle='--')

    # xlim_min = 0.5
    # xlim_max = 1.5
    # plt.xlim(xlim_min, xlim_max)
    # plt.ylim(0, max([errors[i] for i in range(len(errors)) if xlim_min <= c_values[i] <= xlim_max])/2)
    plt.xlabel('c ($s^{-1}$)')
    plt.ylabel('ECM')

    plt.legend(loc='upper right')

    # print(filtered_data.index[0], filtered_data.iloc[0]['average'])
    # print(filtered_data.index[-1], filtered_data.iloc[-1]['average'])

    print(f"Execution time: {time.time() - start_time:.2f}s")
    plt.savefig("analysis/caudal_error.png", dpi=300)
