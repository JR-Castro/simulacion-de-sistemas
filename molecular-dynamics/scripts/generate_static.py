import sys


MAX_TIME = 100
AMPLITUDE = 0.01
N = 100
DT2 = 0.01
MASS = 0.001

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: generate_static.py <k> <w> <output_file>")
        sys.exit(1)

    k = float(sys.argv[1])
    w = float(sys.argv[2])
    output_file = sys.argv[3]

    with open(output_file, 'w') as f:
        f.write(f"{MAX_TIME}\n")
        f.write(f"{k}\n")
        f.write(f"{AMPLITUDE}\n")
        f.write(f"{N}\n")
        f.write(f"{w}\n")
        f.write(f"{min(1E-3, 1 / (100 * w))}\n")
        f.write(f"{DT2}\n")
        f.write(f"{MASS}\n")