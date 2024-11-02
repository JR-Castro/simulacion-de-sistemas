import os
import subprocess

from generate_inputs import RUNS

CMD = "java -jar target/main.jar "

if __name__ == '__main__':
    # Check if dir exists
    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    subprocess.run(CMD + f" ./inputs/static/1.json {''.join([f'./inputs/dynamic/1_{i}.json ' for i in range(RUNS)])}",
                   shell=True)

    # Run rest of tests
    # Maybe change main to take <static1> <dynamic1> <static2> <dynamic2> so we can run all tests at once




