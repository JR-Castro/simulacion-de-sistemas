import math
import os
import sys

MAX_TIME = 120
AMPLITUDE = 0.01
N = 100
DT2 = 0.01
MASS = 0.001
DEFAULT_K = 100.0
K_VALUES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

RUNS = 5


def optimum_w(k):
    return math.pi / (N + 1) * math.sqrt(k / MASS)


def calculate_test_w_values(k):
    w0 = optimum_w(k)
    start = 0.9 * w0  # Narrow the range closer to w0
    end = 1.1 * w0
    return [start + (end - start) * j / (RUNS - 1) for j in range(RUNS)]


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
            f.write(f"{MAX_TIME}\n")
            f.write(f"{DEFAULT_K}\n")
            f.write(f"{AMPLITUDE}\n")
            f.write(f"{N}\n")
            f.write(f"{w}\n")
            f.write(f"{min(1E-3, 1 / (100 * w))}\n")
            f.write(f"{DT2}\n")
            f.write(f"{MASS}\n")

    for i, k in enumerate(K_VALUES):
        for j, w in enumerate(calculate_test_w_values(k)):
            with open(f"{output_path}/k{i}_{j}.txt", 'w') as f:
                f.write(f"{MAX_TIME}\n")
                f.write(f"{k}\n")
                f.write(f"{AMPLITUDE}\n")
                f.write(f"{N}\n")
                f.write(f"{w}\n")
                f.write(f"{min(1E-3, 1 / (100 * w))}\n")
                f.write(f"{DT2}\n")
                f.write(f"{MASS}\n")
