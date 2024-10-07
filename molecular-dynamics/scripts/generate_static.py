import math
import os

MAX_TIME = 120
AMPLITUDE = 10E-2
N = 100
DT2 = 0.05
MASS = 0.001
DEFAULT_K = 100.0
K_VALUES = [100, 250, 500, 750, 1000]
OPTIMUM_W_VALUES = [10.0, 15.5, 22.0, 27.0, 31.0]
TEST_W_VALUES = {
    K_VALUES[0]: (7.5,12.5),
    K_VALUES[1]: (12.5,17.5),
    K_VALUES[2]: (20,25),
    K_VALUES[3]: (25,30),
    K_VALUES[4]: (30,35)
}

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
    if k in K_VALUES:
        start, end = TEST_W_VALUES[k]
    else:
        start = w0 - 5
        end = w0 + 5
    step = (end - start) / (RUNS - 1)

    return [start + i * step for i in range(RUNS)]


if __name__ == '__main__':
    output_dir = 'static'
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
