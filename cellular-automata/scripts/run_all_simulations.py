import re
import subprocess
import time
from os import listdir
from os.path import isfile, join
from pathlib import Path

from utils import STATIC_2D_PATH, STATIC_3D_PATH, OUTPUT_2D_PATH, OUTPUT_3D_PATH, DYNAMIC_2D_PATH, RUN_SIMULATION_CMD, \
    DYNAMIC_3D_PATH, STATIC_FILES_2D, STATIC_FILES_3D


def run_simulation(cmd):
    subprocess.run(cmd, shell=True, check=True)


if __name__ == '__main__':
    Path(OUTPUT_2D_PATH).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_3D_PATH).mkdir(parents=True, exist_ok=True)

    start_time = time.time()

    for file in STATIC_FILES_2D:
        dynamic_files = [f for f in listdir(DYNAMIC_2D_PATH) if
                         isfile(join(DYNAMIC_2D_PATH, f)) and re.match(f"[0-9]", f)]

        dynamic_files_paths = ",".join([join(DYNAMIC_2D_PATH, dynamic_file) for dynamic_file in dynamic_files])
        output_files_paths = ",".join(
            [join(OUTPUT_2D_PATH, f"{file.split('.')[0]}_{dynamic_input_file}") for dynamic_input_file in dynamic_files])
        print(f'Running 2d simulation for {file} with {len(dynamic_files)} dynamic files')
        run_simulation(
            f'{RUN_SIMULATION_CMD} {join(STATIC_2D_PATH, file)} {dynamic_files_paths} {output_files_paths}'
        )

    for file in STATIC_FILES_3D:
        dynamic_files = [f for f in listdir(DYNAMIC_2D_PATH) if
                         isfile(join(DYNAMIC_2D_PATH, f)) and re.match(f"[0-9]", f)]
        dynamic_files_paths = ",".join([join(DYNAMIC_3D_PATH, dynamic_file) for dynamic_file in dynamic_files])
        output_files_paths = ",".join(
            [join(OUTPUT_3D_PATH, f"{file.split('.')[0]}_{dynamic_input_file}") for dynamic_input_file in dynamic_files])
        print(f'Running 3d simulation for {file} with {len(dynamic_files)} dynamic files')
        run_simulation(
            f'{RUN_SIMULATION_CMD} {join(STATIC_3D_PATH, file)} {dynamic_files_paths} {output_files_paths}'
        )

    print(f'--- {time.time() - start_time} seconds ---')
