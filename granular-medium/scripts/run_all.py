import os
import subprocess

from generate_inputs import RUNS, A0_VALUES, M_VALUES

CMD = "java -jar target/main.jar --no-states "

if __name__ == '__main__':
    # Check if dir exists
    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    c_cmd = " "
    for i in range(len(M_VALUES)):
        for j in range(len(A0_VALUES)):
            c_cmd += "".join(
                [f" ./inputs/static/3_{i}_{j}.json ./inputs/dynamic/3_{i}_{j}_{k}.json " for k in range(RUNS)])

    print("Running cmd: ", c_cmd)
    subprocess.run(CMD + c_cmd, shell=True)
