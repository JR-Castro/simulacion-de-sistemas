import os
import subprocess

from generate_inputs import RUNS, A0_VALUES, M_VALUES

CMD = "java -jar target/main.jar --no-states "

if __name__ == '__main__':
    # Check if dir exists
    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    # A
    a_cmd = ''.join([f" ./inputs/static/1.json ./inputs/dynamic/1_{i}.json " for i in range(RUNS)])

    print("Running cmd: ", a_cmd)
    subprocess.run(CMD + a_cmd,
                   shell=True)

    # B
    b_cmd = " "
    for i in range(len(A0_VALUES)):
        b_cmd += "".join([f" ./inputs/static/2_{i}.json ./inputs/dynamic/2_{i}_{j}.json " for j in range(RUNS)])

    print("Running cmd: ", b_cmd)
    subprocess.run(CMD + b_cmd, shell=True)

    # C
    c_cmd = " "
    for i in range(len(M_VALUES)):
        for j in range(len(A0_VALUES)):
            c_cmd += "".join(
                [f" ./inputs/static/3_{i}_{j}.json ./inputs/dynamic/3_{i}_{j}_{k}.json " for k in range(RUNS)])

    print("Running cmd: ", c_cmd)
    subprocess.run(CMD + c_cmd, shell=True)
