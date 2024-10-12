import math
import os

MAX_TIME = 120
AMPLITUDE = 10E-2
N = 100
DT2 = 0.05
MASS = 0.001
DEFAULT_K = 100.0
K_VALUES = [100, 1000, 2500, 5000, 10000]
OPTIMUM_W_VALUES = [10.0, 31.0, 49.0, 70.0, 98.0]
TEST_W_VALUES = {
    K_VALUES[0]: (7.5,12.5),
    K_VALUES[1]: (28.5,33.5),
    K_VALUES[2]: (46.5,51.5),
    K_VALUES[3]: (67.5,72.5),
    K_VALUES[4]: (95.5,100.5)
}

RUNS = 20


def optimum_w(k):
    return math.pi / (N + 1) * math.sqrt(k / MASS)

def get_max_time(k):
    if k <= 500:
        return 100
    elif k < 1000:
        return 50
    else:
        return 120

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
