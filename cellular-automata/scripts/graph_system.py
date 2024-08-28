import json
import sys
import matplotlib.pyplot as plt
import numpy as np


def graph_cells_alive(data):
    steps = range(len(data))
    cells_alive = [len(frame["cells"]) for frame in data]

    plt.plot(steps, cells_alive)
    plt.ylabel("Cells alive")
    plt.xlabel("Step")
    plt.legend()
    plt.show()


def graph_max_distance(data, static):
    center = static["areaSize"] // 2

    max_distances = []
    for frame in data:
        cells = frame["cells"]
        distances = [
            np.sqrt((cell["x"] - center)**2 +
                    (cell["y"] - center)**2 +
                    (cell["z"] - center)**2) for cell in cells
        ]
        max_distances.append(max(distances))

    steps = range(len(data))

    plt.plot(steps, max_distances)
    plt.ylabel("Max Distance from center")
    plt.xlabel("Step")
    plt.legend()
    plt.show()


def graph_all_metrics(data, static):
    steps = range(len(data))

    cells_alive = [len(frame["cells"]) for frame in data]

    center = static["areaSize"] // 2
    max_distances = []
    for frame in data:
        cells = frame["cells"]
        distances = [
            np.sqrt((cell["x"] - center)**2 +
                    (cell["y"] - center)**2 +
                    (cell["z"] - center)**2) for cell in cells
        ]
        max_distances.append(max(distances))

    plt.figure(figsize=(10, 6))
    plt.plot(steps, cells_alive, label="Cells alive")
    plt.plot(steps, max_distances, label="Max Distance from center")

    plt.xlabel("Step")
    plt.ylabel("Values")
    plt.legend()
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
    graph_max_distance(data, static)
