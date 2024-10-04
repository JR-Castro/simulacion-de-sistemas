import math
import sys


MAX_TIME = 100
AMPLITUDE = 0.01
N = 100
DT2 = 0.01
MASS = 0.001
DEFAULT_K = 100.0
W_VALUES = [9.0, 9.25, 9.5, 9.75, 10.0, 10.25, 10.5, 10.75, 11.0]
K_VALUES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

RUNS = 5

def optimum_w(k):
    return math.pi / (N+1) * math.sqrt(k / MASS)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: generate_static.py <output_path>")
        sys.exit(1)

    output_path = sys.argv[1]


    for i, w in enumerate(W_VALUES):
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
        w0 = optimum_w(k)
        start = 0.5 * w0
        end = 1.5 * w0
        for j in range(RUNS):
            w = start + (end - start) * j / (RUNS - 1)
            with open(f"{output_path}/k{i}_{j}.txt", 'w') as f:
                f.write(f"{MAX_TIME}\n")
                f.write(f"{k}\n")
                f.write(f"{AMPLITUDE}\n")
                f.write(f"{N}\n")
                f.write(f"{w}\n")
                f.write(f"{min(1E-3, 1 / (100 * w))}\n")
                f.write(f"{DT2}\n")
                f.write(f"{MASS}\n")
