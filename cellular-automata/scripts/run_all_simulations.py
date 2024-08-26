import subprocess
from os import listdir
from os.path import isfile, join
from pathlib import Path

static_3d_path = '../src/main/resources/static/3d'
static_2d_path = '../src/main/resources/static/2d'

dynamic_3d_path = '../src/main/resources/dynamic/3d'
dynamic_2d_path = '../src/main/resources/dynamic/2d'

output_2d_path = '../output/2d'
output_3d_path = '../output/3d'

run_simulation_cmd = 'java -jar ../target/cellular-automata-1.0-SNAPSHOT-jar-with-dependencies.jar'

if __name__ == '__main__':
    static_files_2d = [f for f in listdir(static_2d_path) if isfile(join(static_2d_path, f))]
    static_files_3d = [f for f in listdir(static_3d_path) if isfile(join(static_3d_path, f))]

    Path(output_2d_path).mkdir(parents=True, exist_ok=True)
    Path(output_3d_path).mkdir(parents=True, exist_ok=True)

    for file in static_files_2d:
        dynamic_files = [f for f in listdir(dynamic_2d_path) if
                         isfile(join(dynamic_2d_path, f)) and f.startswith(file.split('.')[0])]
        for dynamic_file in dynamic_files:
            print(f'Running 2d simulation for {file} with {dynamic_file}')
            dynamic_2d_file_name = dynamic_file.split('.')[0]
            proc = subprocess.run(
                f'{run_simulation_cmd} {join(static_2d_path, file)} {join(dynamic_2d_path, dynamic_file)} {join(output_2d_path, dynamic_2d_file_name)}',
                shell=True, check=True)

    for file in static_files_3d:
        dynamic_files = [f for f in listdir(dynamic_3d_path) if
                         isfile(join(dynamic_3d_path, f)) and f.startswith(file.split('.')[0])]
        for dynamic_file in dynamic_files:
            print(f'Running 3d simulation for {file} with {dynamic_file}')
            dynamic_3d_file_name = dynamic_file.split('.')[0]
            proc = subprocess.run(
                f'{run_simulation_cmd} {join(static_3d_path, file)} {join(dynamic_3d_path, dynamic_file)} {join(output_3d_path, dynamic_3d_file_name)}',
                shell=True, check=True)
