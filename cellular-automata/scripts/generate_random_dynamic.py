import json
import random
from os.path import join
from pathlib import Path

from utils import DYNAMIC_3D_PATH, DYNAMIC_2D_PATH, STATIC_2D_PATH, STATIC_3D_PATH, RUN_ITERATIONS, STATIC_FILES_2D, \
    STATIC_FILES_3D, PERCENTAGES


def generate_random_dynamic(static_data, is3d: bool, file_name, center_size: int = 10, percentage: float = 0.1):
    center = static_data['areaSize'] // 2

    cells = []

    cells_ammount = int(center_size ** (3 if is3d else 2) * percentage)

    if is3d:
        for i in range(cells_ammount):
            cells.append((random.randint(center - center_size, center + center_size),
                          random.randint(center - center_size, center + center_size),
                          random.randint(center - center_size, center + center_size)))
    else:
        for i in range(cells_ammount):
            cells.append((random.randint(center - center_size, center + center_size),
                          random.randint(center - center_size, center + center_size),
                          0))

    dynamic_data = {
        "moments": [{
            "time": 0,
            "cells": [
                {"x": x, "y": y, "z": z, "state": 1} for x, y, z in cells
            ]
        }]
    }

    with open(join(DYNAMIC_3D_PATH if is3d else DYNAMIC_2D_PATH, file_name), 'w') as f:
        json.dump(dynamic_data, f, indent=4)


if __name__ == '__main__':
    Path(DYNAMIC_2D_PATH).mkdir(parents=True, exist_ok=True)
    Path(DYNAMIC_3D_PATH).mkdir(parents=True, exist_ok=True)

    for file in STATIC_FILES_2D:
        with open(join(STATIC_2D_PATH, file)) as f:
            static_data = json.load(f)

            for percentage in PERCENTAGES:
                for j in range(RUN_ITERATIONS):
                    generate_random_dynamic(static_data, False, f"{file.split('.')[0]}_{int(percentage*100)}_{j}.json", percentage=percentage)

    for file in STATIC_FILES_3D:
        with open(join(STATIC_3D_PATH, file)) as f:
            static_data = json.load(f)

            for percentage in PERCENTAGES:
                for j in range(RUN_ITERATIONS):
                    generate_random_dynamic(static_data, True, f"{file.split('.')[0]}_{int(percentage*100)}_{j}.json", percentage=percentage)
