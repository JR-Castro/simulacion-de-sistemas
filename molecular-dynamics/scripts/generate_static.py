import math
import os

MAX_TIME = 120
AMPLITUDE = 10E-2
N = 100
DT2 = 0.05
MASS = 0.001
DEFAULT_K = 100.0
K_VALUES = [100, 1000, 2500, 5000, 7500, 10000]
OPTIMUM_W_VALUES = [10.0, 31.0, 49.0, 70.0, 85.0, 98.0]
TEST_W_VALUES = {
    K_VALUES[0]: (7.5, 12.5),
    K_VALUES[1]: (28.5, 33.5),
    K_VALUES[2]: (46.5, 51.5),
    K_VALUES[3]: (67.5, 72.5),
    K_VALUES[4]: (82.5, 87.5),
    K_VALUES[5]: (95.5, 100.5)
}
ANIM_K = [100, 10000]
ANIM_W = [10, 100]
ANIM_DT2 = [1 / 24, 1 / 120]

RUNS = 20


def optimum_w(k):
    return math.pi / (N + 1) * math.sqrt(k / MASS)


def get_max_time(k):
    if k <= 100:
        return 80
    elif 100 < k <= 1500:
        return 130
    elif 1500 < k <= 2750:
        return 250
    elif 2750 < k:
        return 60


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

    for i in range(len(ANIM_K)):
        with open(f"{output_path}/anim_{i}.txt", 'w') as f:
            f.write(f"{get_max_time(ANIM_K[i])}\n")
            f.write(f"{ANIM_K[i]}\n")
            f.write(f"{AMPLITUDE}\n")
            f.write(f"{N}\n")
            f.write(f"{ANIM_W[i]}\n")
            f.write(f"{get_dt(ANIM_W[i])}\n")
            f.write(f"{ANIM_DT2[i]}\n")
            f.write(f"{MASS}\n")
