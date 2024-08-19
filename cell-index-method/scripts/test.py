import os
import re
import subprocess
import numpy as np
import plotly.graph_objects as go

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
        proc = subprocess.run(cmd.split())
        if proc.returncode != 0:
            return None
        outputs.append(get_output_state("./tmp.txt"))

    os.remove("./tmp.txt")

    return outputs


if __name__ == '__main__':

    results = {}
    for i in range(1, 100):
        outputs = run_simulation(15, i, 1, '../static.txt', '../dynamic.txt', True)
        if outputs is None:
            # We found an M value that didn't work
            break
        results[i] = [output['time'] for output in outputs]

    means = [np.mean(values) for values in results.values()]
    std_devs = [np.std(values) for values in results.values()]
    categories = list(results.keys())

    # Create bar chart with error bars
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=means,
            error_y=dict(type='data', array=std_devs, visible=True)
        )
    ])

    fig.update_layout(
        title='Time to Execute',
        xaxis_title='M Value',
        yaxis_title='Time (ms)',
        xaxis=dict(tickmode='linear')
    )

    fig.show()
