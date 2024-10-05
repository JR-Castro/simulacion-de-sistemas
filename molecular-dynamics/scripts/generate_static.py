import math
import os
import sys

MAX_TIME = 120
AMPLITUDE = 10E-2
N = 100
DT2 = 0.05
MASS = 0.001
DEFAULT_K = 100.0
K_VALUES = [100, 250, 500, 750, 1000]
OPTIMUM_W_VALUES = [10.0, 15.5, 22.0, 27.0, 31.0]

RUNS = 20


def optimum_w(k):
    return math.pi / (N + 1) * math.sqrt(k / MASS)

def get_max_time(k):
    if k < 251:
        return MAX_TIME
    if k < 750:
        return MAX_TIME + 60
    if k < 900:
        return MAX_TIME + 90
    return 4 * MAX_TIME

def get_dt(w):
    return min(1E-3, 1 / (100 * w))

def calculate_test_w_values(k):
    w0 = OPTIMUM_W_VALUES[K_VALUES.index(k)] if k in K_VALUES else optimum_w(k)
    start = w0 - 1.25
    end = w0 + 1.25
    step = (end - start) / (RUNS - 1)

    return [start + i * step for i in range(RUNS)]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: generate_static.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    # Make sure the dir exists
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs('output', exist_ok=True)
    # Get the absolute path
    output_path = os.path.abspath(output_dir)

    for i, w in enumerate(calculate_test_w_values(DEFAULT_K)):
        with open(f"{output_path}/w{i}.txt", 'w') as f:
            f.write(f"{get_max_time(DEFAULT_K)}\n")
            f.write(f"{DEFAULT_K}\n")
            f.write(f"{AMPLITUDE}\n")
            f.write(f"{N}\n")
            f.write(f"{w}\n")
            f.write(f"{get_dt(w)}\n")
            f.write(f"{DT2}\n")
            f.write(f"{MASS}\n")

    for i, k in enumerate(K_VALUES):
        for j, w in enumerate(calculate_test_w_values(k)):
            with open(f"{output_path}/k{i}_{j}.txt", 'w') as f:
                f.write(f"{get_max_time(k)}\n")
                f.write(f"{k}\n")
                f.write(f"{AMPLITUDE}\n")
                f.write(f"{N}\n")
                f.write(f"{w}\n")
                f.write(f"{get_dt(w)}\n")
                f.write(f"{DT2}\n")
                f.write(f"{MASS}\n")
