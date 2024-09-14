import os
import re
import subprocess
import sys
import time
from os import listdir
from os.path import isfile, join, exists

CMD = 'java -jar ./target/main.jar'

def run_simulation(cmd):
    subprocess.run(cmd, shell=True, check=True)

if __name__ == '__main__':
    # static, dynamic_pattern, output_dir
    if len(sys.argv) < 4:
        print("Usage: run_simulations.py <static_file> <dynamic_file_pattern>")
        sys.exit(1)

    static_file = sys.argv[1]
    dynamic_file_pattern = sys.argv[2]
    output_dir = sys.argv[3]

    # Make output dir if not exists
    if not exists(output_dir):
        os.makedirs(output_dir)

    dynamic_file_pattern_dir = dynamic_file_pattern[:dynamic_file_pattern.rfind('/')]
    dynamic_file_pattern_file = dynamic_file_pattern[dynamic_file_pattern.rfind('/')+1:]

    dynamic_files = [f for f in listdir(dynamic_file_pattern_dir) if isfile(join(dynamic_file_pattern_dir, f)) and re.match(dynamic_file_pattern_file, f)]

    start_time = time.time()

    for df in dynamic_files:
        file_name = ''.join(df.split('.')[:-1])
        cmd = f'{CMD} {static_file} {join(dynamic_file_pattern_dir, df)} {join(output_dir, file_name)}'
        print("Running simulation with command: ", cmd)
        run_simulation(cmd)

    print(f"Total time: {time.time() - start_time}s")