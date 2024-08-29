from itertools import groupby
from math import sqrt
from os import listdir
from os.path import join, isfile
from pathlib import Path
import time
import re
import json
import matplotlib.pyplot as plt
import numpy as np

from utils import OUTPUT_IMAGES_2D_PATH, OUTPUT_IMAGES_3D_PATH, STATIC_FILES_2D, OUTPUT_2D_PATH, STATIC_2D_PATH, \
    extract_first_number, STATIC_FILES_3D, OUTPUT_3D_PATH, STATIC_3D_PATH


def graph_last_cells_alive(all_runs, output_file):
    print("Last Cells Alive")
    plt.figure()
    for run in all_runs:
        percentage_runs = run["data"]
        last_cells_alive = [len(percentage_run[-1]["cells"]) for percentage_run in percentage_runs]
        mean = np.mean(last_cells_alive)
        std = np.std(last_cells_alive, ddof=1)
        print(f"\tPercentage: {run['label']}\n\tMean: {mean}\n\tStd: {std}")
        plt.bar(run["label"], mean, yerr=std, capsize=5)

    plt.xlabel("Porcentaje de células vivas")
    plt.ylabel("Células vivas en ultimo paso")
    plt.savefig(output_file)
    plt.clf()


def graph_last_max_distance(all_runs, output_file):
    print("Last Max Distance")
    plt.figure()
    for run in all_runs:
        percentage_runs = run["data"]
        distances = [[
            sqrt((cell["x"] - 50) ** 2 +
                 (cell["y"] - 50) ** 2 +
                 (cell["z"] - 50) ** 2) for cell in percentage_run[-1]["cells"]
        ] for percentage_run in percentage_runs]
        last_max_distance = [
            max(distance, default=0) for distance in distances
        ]
        mean = np.mean(last_max_distance)
        std = np.std(last_max_distance, ddof=1)
        print(f"\tPercentage: {run['label']}\n\t\tMean: {mean}\n\t\tStd: {std}")
        plt.bar(run["label"], mean, yerr=std, capsize=5)

    plt.xlabel("Porcentaje de células vivas")
    plt.ylabel("Distancia máxima en ultimo paso")
    plt.savefig(output_file)
    plt.clf()


def graph_time_to_reach_border(static, all_runs, output_file):
    print("Time to reach border")
    plt.figure()
    for run in all_runs:
        percentage_runs = run["data"]
        time_to_reach_border = [
            percentage_run.index(percentage_run[-1]) for percentage_run in percentage_runs
        ]
        cells_last_step = [percentage_run[-1]["cells"] for percentage_run in percentage_runs]
        for cells in cells_last_step:
            if not any([cell["x"] == 0 or cell["x"] == static["areaSize"] - 1 or
                        cell["y"] == 0 or cell["y"] == static["areaSize"] - 1 or
                        cell["z"] == 0 or cell["z"] == static["areaSize"] - 1 for cell in cells]):
                print("Not all runs reached the border")
        mean = np.mean(time_to_reach_border)
        std = np.std(time_to_reach_border, ddof=1)
        print(f"\tPercentage: {run['label']}\n\t\tMean: {mean}\n\t\tStd: {std}")
        plt.bar(run["label"], mean, yerr=std, capsize=5)

    plt.xlabel("Porcentaje de células vivas")
    plt.ylabel("Tiempo en pasos para llegar a la frontera")
    plt.savefig(output_file)
    plt.clf()


def get_slope(max_distances):
    x = range(len(max_distances))

    b = max_distances[0]
    slope = 0
    tolerance = 1e-6
    learning_rate = 1e-6

    last_quad_error = float('inf')

    for _ in range(10):
        # Calculate the predictions with the current slope
        predictions = [slope * xi + b for xi in x]

        # Calculate the error (sum of squared differences)
        errors = [(yi - pred) for yi, pred in zip(max_distances, predictions)]
        quad_error = sum(e**2 for e in errors) / len(max_distances)

        # Check if the error is not improving significantly
        if abs(last_quad_error - quad_error) < tolerance:
            break

        last_quad_error = quad_error

        # Calculate the gradient (derivative of the error w.r.t slope)
        gradient = -2 * sum(xi * e for xi, e in zip(x, errors)) / len(max_distances)

        # Update the slope using the gradient
        slope -= learning_rate * gradient

    return slope, b, last_quad_error


def graph_slope_max_distance(static, all_runs, output_file):
    print("Slope Max Distance")
    plt.figure()
    for run in all_runs:
        percentage_runs = run["data"]
        max_distances = [[
            max([
                sqrt((cell["x"] - 50) ** 2 +
                     (cell["y"] - 50) ** 2 +
                     (cell["z"] - 50) ** 2) for cell in frame["cells"]
            ], default=0) for frame in percentage_run
        ] for percentage_run in percentage_runs]
        slopes = []
        start_points = []
        quad_errors = []
        for max_distance in max_distances:
            slope, start, error = get_slope(max_distance)
            slopes.append(slope)
            start_points.append(start)
            quad_errors.append(error)
        mean_slope = np.mean(slopes)
        std_slope = np.std(slopes)
        mean_start_points = np.mean(start_points)
        std_start_points = np.std(start_points, ddof=1)
        mean_quad_errors = np.mean(quad_errors)
        std_quad_errors = np.std(quad_errors, ddof=1)
        print(f"\tPercentage: {run['label']}\n\t\tMean Slope: {mean_slope}\n\t\tStd Slope: {std_slope}\n"
                f"\t\tMean Start Point: {mean_start_points}\n\t\tStd Start Point: {std_start_points}\n"
                f"\t\tMean Quad Error: {mean_quad_errors}\n\t\tStd Quad Error: {std_quad_errors}")
        plt.bar(run["label"], mean_slope, yerr=std_slope, capsize=5)

    plt.xlabel("Porcentaje de células vivas")
    plt.ylabel("Pendiente de la distancia máxima por paso")
    plt.savefig(output_file)
    plt.clf()

def plot_total_growth(all_runs, output_file):
    plt.figure()
    for run_config in all_runs:
        runs = run_config["data"]

        start_cells = [len(run[0]["cells"]) for run in runs]
        end_cells = [len(run[-1]["cells"]) for run in runs]

        ratio = np.divide(np.subtract(end_cells, start_cells), start_cells)
        mean = np.mean(ratio)
        std = np.std(ratio, ddof=1)

        plt.bar(run_config["label"], mean, yerr=std, capsize=5)

    plt.xlabel("Porcentaje inicial de células vivas")
    plt.ylabel("Crecimiento total de celulas vivas")
    plt.savefig(output_file)
    plt.clf()


if __name__ == '__main__':
    Path(OUTPUT_IMAGES_2D_PATH).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_IMAGES_3D_PATH).mkdir(parents=True, exist_ok=True)

    start_time = time.time()

    for file in STATIC_FILES_2D:
        print(f"{file} 2D")
        output_files = [f for f in listdir(OUTPUT_2D_PATH) if
                        isfile(join(OUTPUT_2D_PATH, f)) and re.match(f"{file.split('.')[0]}_[0-9]", f)]

        with open(join(STATIC_2D_PATH, file), 'r') as f:
            static = json.load(f)

        sorted_filenames = sorted(output_files, key=extract_first_number)
        grouped_filenames = {k: list(g) for k, g in groupby(sorted_filenames, key=extract_first_number)}

        all_runs = []
        for key, group in grouped_filenames.items():

            percentage_run = []
            for output_file in group:
                with open(join(OUTPUT_2D_PATH, output_file), 'r') as f:
                    percentage_run.append(json.load(f))

            all_runs.append({"data": percentage_run, "label": f"{key}%"})

        if file == "static_conway.json":
            graph_last_cells_alive(all_runs, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_last_cells_alive.png"))
            # graph_slope_max_distance(static, all_runs, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_slope_max_distance.png"))
        elif file == "static_conway_von_neumann.json":
            graph_slope_max_distance(static, all_runs, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_slope_max_distance.png"))
            graph_last_cells_alive(all_runs, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_last_cells_alive.png"))
        elif file == "static_climbing_plants.json":
            graph_last_cells_alive(all_runs, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_last_cells_alive.png"))
        else:
            print("Invalid file")

        plot_total_growth(all_runs, join(OUTPUT_IMAGES_2D_PATH, f"{file.split('.')[0]}_total_growth.png"))

    for file in STATIC_FILES_3D:
        print(f"{file} 3D")

        output_files = [f for f in listdir(OUTPUT_3D_PATH) if
                        isfile(join(OUTPUT_3D_PATH, f)) and re.match(f"{file.split('.')[0]}_[0-9]", f)]

        with open(join(STATIC_3D_PATH, file), 'r') as f:
            static = json.load(f)

        sorted_filenames = sorted(output_files, key=extract_first_number)
        grouped_filenames = {k: list(g) for k, g in groupby(sorted_filenames, key=extract_first_number)}

        all_runs = []
        for key, group in grouped_filenames.items():

            percentage_run = []
            for output_file in group:
                with open(join(OUTPUT_3D_PATH, output_file), 'r') as f:
                    percentage_run.append(json.load(f))

            all_runs.append({"data": percentage_run, "label": f"{key}%"})

        if file == "static_conway.json":
            # graph_slope_max_distance(static, all_runs, join(OUTPUT_IMAGES_3D_PATH, f"{file.split('.')[0]}_slope_max_distance.png"))
            graph_last_cells_alive(all_runs, join(OUTPUT_IMAGES_3D_PATH, f"{file.split('.')[0]}_last_cells_alive.png"))
        elif file == "static_conway_von_neumann.json":
            graph_last_cells_alive(all_runs, join(OUTPUT_IMAGES_3D_PATH, f"{file.split('.')[0]}_last_cells_alive.png"))
        elif file == "static_climbing_plants.json":
            graph_last_cells_alive(all_runs, join(OUTPUT_IMAGES_3D_PATH, f"{file.split('.')[0]}_last_cells_alive.png"))
        else:
            print("Invalid file")

        plot_total_growth(all_runs, join(OUTPUT_IMAGES_3D_PATH, f"{file.split('.')[0]}_total_growth.png"))
