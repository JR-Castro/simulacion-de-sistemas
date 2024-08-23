import json
import sys

import matplotlib.pyplot as plt


def graph_cells_alive(data):
    plt.plot(range(len(data)), [len(frame["cells"]) for frame in data])
    plt.ylabel("Cells alive")
    plt.xlabel("Step")
    plt.show()


def graph_distance(data, static):
    center = static["areaSize"] // 2

    distances = []
    for frame in data:
        cells = frame["cells"]
        distances.append(
            [abs(cell["x"] - center) + abs(cell["y"] - center) + abs(cell["z"] - center) for cell in cells])

    plt.plot(range(len(data)), [sum(distances[i]) for i in range(len(distances))])
    plt.ylabel("Distance from center")
    plt.xlabel("Step")
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python graph_system.py <data.json> <static.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    with open(sys.argv[2], 'r') as f:
        static = json.load(f)

    graph_cells_alive(data)
    graph_distance(data, static)
