import json
import re
import time
from itertools import groupby
from math import sqrt
from os import listdir
from os.path import join, isfile
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from utils import OUTPUT_2D_PATH, OUTPUT_IMAGES_2D_PATH, OUTPUT_IMAGES_3D_PATH, STATIC_FILES_2D, STATIC_FILES_3D, \
    OUTPUT_3D_PATH, STATIC_2D_PATH, STATIC_3D_PATH


def graph_all_cells_alive(runs, output_file):
    runs_count = np.max([len(run) for run in runs])

    cells = np.vstack([np.pad([len(frame["cells"]) for frame in run], (0, runs_count - len(run))) for run in runs])
    means = cells.mean(axis=0)
    stds = cells.std(axis=0, ddof=1)

    plt.plot(range(runs_count), means, linestyle='--', marker='o')
    plt.fill_between(range(runs_count), means - stds, means + stds, alpha=0.3)

    plt.xlabel("Step")
    plt.ylabel("Cells alive")
    plt.savefig(output_file)
    plt.clf()


def graph_all_max_distance(runs, static, output_file):
    runs_count = np.max([len(run) for run in runs])
    center = static["areaSize"] // 2

    max_distances = np.vstack([np.pad([ max([
        sqrt((cell["x"] - center)**2 +
             (cell["y"] - center)**2 +
             (cell["z"] - center)**2) for cell in frame["cells"]
    ], default=0) for frame in run], (0, runs_count - len(run))) for run in runs])
    means = max_distances.mean(axis=0)
    stds = max_distances.std(axis=0, ddof=1)

    plt.plot(range(runs_count), means, linestyle='--', marker='o')
    plt.fill_between(range(runs_count), means - stds, means + stds, alpha=0.3)

    plt.xlabel("Step")
    plt.ylabel("Max Distance from center")
    plt.savefig(output_file)
    plt.clf()


def extract_first_number(filename):
    match = re.search(r'_(\d+)_', filename)
    return int(match.group(1)) if match else None


if __name__ == '__main__':
    Path(OUTPUT_IMAGES_2D_PATH).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_IMAGES_3D_PATH).mkdir(parents=True, exist_ok=True)

    start_time = time.time()

    for file in STATIC_FILES_2D:
        output_files = [f for f in listdir(OUTPUT_2D_PATH) if
                        isfile(join(OUTPUT_2D_PATH, f)) and re.match(f"{file.split('.')[0]}_[0-9]", f)]

        with open(join(STATIC_2D_PATH, file), 'r') as f:
            static = json.load(f)

        sorted_filenames = sorted(output_files, key=extract_first_number)
        grouped_filenames = {k: list(g) for k, g in groupby(sorted_filenames, key=extract_first_number)}

        for key, group in grouped_filenames.items():
            runs = []

            for output_file in group:
                with open(join(OUTPUT_2D_PATH, output_file), 'r') as f:
                    runs.append(json.load(f))

            graph_all_cells_alive(runs, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_{key}_cells_alive.png"))
            graph_all_max_distance(runs, static, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_{key}_max_distance.png"))

    for file in STATIC_FILES_3D:
        output_files = [f for f in listdir(OUTPUT_3D_PATH) if
                        isfile(join(OUTPUT_3D_PATH, f)) and re.match(f"{file.split('.')[0]}_[0-9]", f)]

        with open(join(STATIC_3D_PATH, file), 'r') as f:
            static = json.load(f)

        sorted_filenames = sorted(output_files, key=extract_first_number)
        grouped_filenames = {k: list(g) for k, g in groupby(sorted_filenames, key=extract_first_number)}

        for key, group in grouped_filenames.items():
            runs = []

            for output_file in group:
                with open(join(OUTPUT_3D_PATH, output_file), 'r') as f:
                    runs.append(json.load(f))

            graph_all_cells_alive(runs, join(OUTPUT_IMAGES_3D_PATH, f"{file.split('.')[0]}_{key}_cells_alive.png"))
            graph_all_max_distance(runs, static, join(OUTPUT_IMAGES_3D_PATH, f"{file.split('.')[0]}_{key}_max_distance.png"))
