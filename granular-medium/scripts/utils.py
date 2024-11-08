import numpy as np
from matplotlib import ticker

FONT = {'size': 14}

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


def calculate_q(exits_data, steady_state, min=0.0, max=2.0, tries=200):
    filtered_data = exits_data[exits_data.index > steady_state]

    x_values = filtered_data.index
    y_values = filtered_data

    x0 = x_values[0]
    y0 = y_values.iloc[0]

    q_values = np.linspace(min, max, tries)

    fit_x_values = x_values - x_values[0]
    fit_y_values = y_values - y0

    q_errors = [compute_mean_square_error(q_val, fit_x_values, fit_y_values) for q_val in q_values]

    min_error_idx = np.argmin(q_errors)
    min_error = q_errors[min_error_idx]

    best_q = q_values[min_error_idx]

    return x0, y0, best_q, min_error
