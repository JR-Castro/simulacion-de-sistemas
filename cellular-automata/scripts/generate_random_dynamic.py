import json
import random
from os import listdir
from os.path import isfile, join
from pathlib import Path

static_3d_path = '../src/main/resources/static/3d'
static_2d_path = '../src/main/resources/static/2d'

dynamic_3d_path = '../src/main/resources/dynamic/3d'
dynamic_2d_path = '../src/main/resources/dynamic/2d'

iterations = 10


def generate_random_dynamic(static_data, is3d: bool, file_name, center_size: int = 10, percentage: float = 0.1):
    center = static_data['areaSize'] // 2

    cells = []

    if is3d:
        for i in range(center - center_size, center + center_size):
            for j in range(center - center_size, center + center_size):
                for k in range(center - center_size, center + center_size):
                    if random.random() < percentage:
                        cells.append((i, j, k))
    else:
        for i in range(center - center_size, center + center_size):
            for j in range(center - center_size, center + center_size):
                if random.random() < percentage:
                    cells.append((i, j, 0))

    dynamic_data = {
        "moments": [{
            "time": 0,
            "cells": [
                {"x": x, "y": y, "z": z} for x, y, z in cells
            ]
        }]
    }

    with open(join(dynamic_3d_path if is3d else dynamic_2d_path, file_name), 'w') as f:
        json.dump(dynamic_data, f, indent=4)


if __name__ == '__main__':
    static_files_2d = [f for f in listdir(static_2d_path) if isfile(join(static_2d_path, f))]
    static_files_3d = [f for f in listdir(static_3d_path) if isfile(join(static_3d_path, f))]

    Path(dynamic_2d_path).mkdir(parents=True, exist_ok=True)
    Path(dynamic_3d_path).mkdir(parents=True, exist_ok=True)

    for file in static_files_2d:
        with open(join(static_2d_path, file)) as f:
            static_data = json.load(f)

            for i in range(10):
                percentage = i * 0.1
                for j in range(iterations):
                    generate_random_dynamic(static_data, False, f"{file.split('.')[0]}_{j}.json", percentage=percentage)

    for file in static_files_3d:
        with open(join(static_3d_path, file)) as f:
            static_data = json.load(f)

            for i in range(10):
                percentage = i * 0.1
                for j in range(iterations):
                    generate_random_dynamic(static_data, True, f"{file.split('.')[0]}_{j}.json", percentage=percentage)
