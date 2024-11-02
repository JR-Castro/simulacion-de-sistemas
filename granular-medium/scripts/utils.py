import numpy as np
from matplotlib import ticker


def formatter(value, pos):
    exponent = int(np.floor(np.log10(abs(value)))) if value != 0 else 0
    coeff = value / 10 ** exponent
    return f'${coeff:.2f} \\times 10^{{{exponent}}}$'

def set_axis_formatter(ax):
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(formatter))
