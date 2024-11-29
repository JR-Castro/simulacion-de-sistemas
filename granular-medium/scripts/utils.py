import numpy as np
import pandas as pd
from matplotlib import ticker
from scipy.optimize import minimize_scalar

from generate_inputs import RUNS

FONT = {'size': 14}
COLORS = ['blue', 'red', 'green', 'purple', 'orange', 'black', 'brown', 'pink', 'gray', 'cyan']
Q_ERROR_POINTS = 20


def formatter(value, pos):
    exponent = int(np.floor(np.log10(abs(value)))) if value != 0 else 0
    coeff = value / 10 ** exponent
    return f'${coeff:.2f} \\times 10^{{{exponent}}}$'


def set_axis_formatter(ax):
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))


def compute_mean_square_error(q, x_values, real):
    predicted = [q * x for x in x_values]
    squared_errors = [(p - r) ** 2 for p, r in zip(predicted, real)]
    return sum(squared_errors) / len(squared_errors)


def get_runs_crossings_from_csv(prefix: str, static_data) -> pd.DataFrame:
    dt = static_data["dt"]
    total_time = static_data['time']
    time_points = [i * dt for i in range(int(total_time / dt))]
    runs_data = pd.DataFrame(index=time_points)

    for i in range(RUNS):
        exits = pd.read_csv(f"{prefix}_{i}_exits.csv")
        exits['time'] = (exits['time'] / dt).round() * dt

        crossings_count = exits['time'].value_counts().reindex(time_points, fill_value=0)
        runs_data[f'run_{i}'] = crossings_count.cumsum()

    return runs_data


def get_filtered_run_data(runs_data, run, steady_state):
    filtered_data = runs_data[runs_data.index > steady_state][run]

    x_values = filtered_data.index
    y_values = filtered_data

    x0 = x_values[0]
    y0 = y_values.iloc[0]

    fit_x_values = x_values - x0
    fit_y_values = y_values - y0
    return x_values , fit_x_values, fit_y_values, x0, y0


def calculate_best_q(x_values, y_values, min=0.0, max=2.0):
    def mse_for_q(q):
        return compute_mean_square_error(q, x_values, y_values)

    result = minimize_scalar(mse_for_q, bounds=(min, max), method='bounded')

    best_q = result.x
    min_error = result.fun

    return best_q, min_error
