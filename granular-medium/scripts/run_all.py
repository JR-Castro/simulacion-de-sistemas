import os
import subprocess

from generate_inputs import RUNS, A0_VALUES, M_VALUES

CMD = "java -jar target/main.jar "

if __name__ == '__main__':
    # Check if dir exists
    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    subprocess.run(CMD + f" ./inputs/static/1.json {''.join([f'./inputs/dynamic/1_{i}.json ' for i in range(RUNS)])}",
                   shell=True)

    # Run rest of tests
    # Maybe change main to take <static1> <dynamic1> <static2> <dynamic2> so we can run all tests at once

    for i in range(len(A0_VALUES)):
        subprocess.run(CMD + f" ./inputs/static/2_{i}.json {''.join([f'./inputs/dynamic/2_{i}_{j}.json ' for j in range(RUNS)])}",
                       shell=True)
        # delete file
        os.remove(f"./outputs/2_{i}_exits.csv")

    for i in range(len(M_VALUES)):
        subprocess.run(CMD + f" ./inputs/static/3_{i}.json {''.join([f'./inputs/dynamic/3_{i}_{j}.json ' for j in range(RUNS)])}",
                       shell=True)

        # delete file
        os.remove(f"./outputs/3_{i}_exits.csv")



