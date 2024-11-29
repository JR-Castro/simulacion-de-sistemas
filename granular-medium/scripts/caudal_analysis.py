import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np

from generate_inputs import RUNS, A0_VALUES, DEFAULT_A0, M_VALUES, DEFAULT_M
from utils import FONT, get_runs_crossings_from_csv, Q_ERROR_POINTS, get_filtered_run_data, calculate_best_q, \
    compute_mean_square_error, COLORS

if __name__ == '__main__':
    start_time = time.time()

    os.makedirs("analysis", exist_ok=True)

    a0_index = A0_VALUES.index(DEFAULT_A0)
    m_index = M_VALUES.index(DEFAULT_M)

    with open(f"inputs/static/3_{m_index}_{a0_index}.json") as f:
        static_data = json.load(f)

    runs_data = get_runs_crossings_from_csv(f"outputs/3_{m_index}_{a0_index}", static_data)

    plt.figure(figsize=(10, 6))

    # y0s = []
    best_qs = []
    run_min_error_idx = []
    run_fit_x_values = []
    run_errors = []
    run_y0_values = []
    run_q_values = []

    xlim_error_min = 0.6
    xlim_error_max = 1.1
    ylim_error_min = 0.0
    # ylim_error_max = 0.0
    ylim_error_max = 25.0
    steady_state = 200.0
    filtered_x = None
    fit_x = None

    for i, run in enumerate(runs_data):
        print(f"Run {i}:")

        # First state where at least one particle crossed
        filt_x, fit_x_values, fit_y_values, x0, y0 = get_filtered_run_data(runs_data, run, steady_state)

        if filtered_x is None:
            filtered_x = filt_x
            fit_x = fit_x_values

        run_y0_values.append(y0)

        best_q, min_error = calculate_best_q(fit_x_values, fit_y_values)

        q_values = np.linspace(best_q - 0.02, best_q + 0.02, Q_ERROR_POINTS)
        run_q_values.append(q_values)

        errors = [compute_mean_square_error(q, fit_x_values, fit_y_values) for q in q_values]
        run_errors.append(errors)

        # Since we are using scipy.optimize.minimize_scalar to find the best q fast, we need to add it
        # to the q_values to make the graph showing we did it as the professor asked
        insert_idx = np.searchsorted(q_values, best_q)
        q_values = np.insert(q_values, insert_idx, best_q)
        q_errors = np.insert(errors, insert_idx, min_error)

        run_min_error_idx.append(insert_idx)

        # ylim_error_max = max(ylim_error_max, max(
        #     error for i, error in enumerate(errors) if xlim_error_min <= q_values[i] <= xlim_error_max))

        q_fit = float(q_values[insert_idx])
        best_qs.append(q_fit)

        print(f"Best fit {i}: q = {q_fit}")
        print(f"Error {i}: {errors[insert_idx]}")

        # Plotting
        plt.plot(runs_data.index, runs_data[run], label=i, color=COLORS[i])

    plt.xlabel("Tiempo (s)", fontdict=FONT)
    plt.ylabel("Partículas", fontdict=FONT)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("analysis/caudal.png", dpi=300)
    plt.clf()

    plt.figure(figsize=(10, 6))
    for i, run in enumerate(runs_data):
        plt.plot(runs_data.index, runs_data[run], alpha=0.5, color=COLORS[i])
        plt.plot(filtered_x,
                 [best_qs[i] * fit_x[j] + run_y0_values[i] for j in range(len(fit_x))],
                 linestyle='--', color=COLORS[i],
                 label=f"$S = {best_qs[i]:.3f} \\, \\mathrm{{s^{{-1}}}} (t - {steady_state} \\,\\mathrm{{s}}) + {run_y0_values[i]}$")

    plt.xlabel("Tiempo ($\\mathrm{s}$)", fontdict=FONT)
    plt.ylabel("Partículas", fontdict=FONT)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.savefig("analysis/caudal_line_fits.png", dpi=300)
    plt.clf()

    plt.figure(figsize=(10, 6))
    # ax = plt.gca()
    # ax.yaxis.set_major_formatter(formatter)

    for i in range(RUNS):
        plt.plot(run_q_values[i], run_errors[i], label=i, marker='.', color=COLORS[i])
        plt.plot(run_q_values[i][run_min_error_idx[i]], run_errors[i][run_min_error_idx[i]], linestyle='', marker='o',
                 # label=f"c = {best_cs[i]:.3f}",
                 color=COLORS[i])

    # plt.axvline(x=c_fit, color='grey', linestyle='--')
    # plt.axhline(y=min(errors), color='grey', linestyle='--')

    # plt.xlim(xlim_error_min, xlim_error_max)
    # plt.ylim(ylim_error_min, ylim_error_max)
    plt.xlabel('$Q \\; (\\mathrm{s^{-1}})$', fontdict=FONT)
    plt.ylabel('ECM', fontdict=FONT)

    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # print(filtered_data.index[0], filtered_data.iloc[0]['average'])
    # print(filtered_data.index[-1], filtered_data.iloc[-1]['average'])

    print(f"Execution time: {time.time() - start_time:.2f}s")
    plt.savefig("analysis/caudal_error.png", dpi=300)
