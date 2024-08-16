import os
import re
import subprocess

def get_output_state(output_file):
    state = {}
    with open(output_file, 'r') as f:
        first_line = f.readline()
        state['time'] = int(first_line.strip())
        state['neighbors'] = []
        for file_line in f:
            particles = re.sub(' +', ' ', file_line).split()
            curr_part = particles[0]
            state['neighbors'].append(particles.remove(curr_part))

    return state

def run_simulation(iters, m, rc, static, dynamic, periodic):
    cmd = f"java -classpath ../target/classes ar.edu.itba.ss.App -static {static} -dynamic {dynamic} -output ./tmp.txt "
    if m:
        cmd = cmd + f" -m {m} "
    if rc:
        cmd = cmd + f" -rc {rc} "
    if periodic:
        cmd = cmd + f" -periodic "

    print(f"Command to run: {cmd}")

    outputs = []
    for i in range(iters):
        subprocess.run(cmd.split())
        outputs.append(get_output_state("./tmp.txt"))

    os.remove("./tmp.txt")

    return outputs


if __name__ == '__main__':
    outputs = run_simulation(10, 3, 0.1, '../src/main/resources/Static100.txt', '../src/main/resources/Dynamic100.txt', True)

    total_time = 0
    for output in outputs:
        total_time += output['time']

    total_time /= len(outputs)
    print("Avg time: ", total_time)

