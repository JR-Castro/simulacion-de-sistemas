import json
import sys
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def calculate_distance_2d(cell, center_pos):
    return np.sqrt((cell['x'] - center_pos[0]) ** 2 + (cell['y'] - center_pos[1]) ** 2)


def calculate_distance_3d(cell, center_pos):
    return np.sqrt(
        (cell['x'] - center_pos[0]) ** 2 + (cell['y'] - center_pos[1]) ** 2 + (cell.get('z', 0) - center_pos[2]) ** 2)


def map_distance_to_color(distance, max_distance):
    # Map the distance to a value between 0 and 1
    normalized_distance = distance / max_distance
    # Create a color gradient from blue (0) to red (1)
    return plt.cm.viridis(normalized_distance)


def plot_2d(ax, cells, center_pos, max_distance, areaSize):
    ax.clear()
    for cell in cells:
        distance = calculate_distance_2d(cell, center_pos)
        color = map_distance_to_color(distance, max_distance)
        rect = plt.Rectangle((cell['x'], cell['y']), 1, 1, color=color)
        ax.add_patch(rect)
    ax.set_xlim(0, areaSize)
    ax.set_ylim(0, areaSize)
    ax.set_aspect('equal')


def plot_3d(ax, cells, center_pos, max_distance, areaSize):
    ax.clear()
    for cell in cells:
        distance = calculate_distance_3d(cell, center_pos)
        color = map_distance_to_color(distance, max_distance)
        ax.bar3d(cell['x'], cell['y'], cell.get('z', 0), 1, 1, 1, color=color)
    ax.set_xlim(0, areaSize)
    ax.set_ylim(0, areaSize)
    ax.set_zlim(0, areaSize)


def update_2d(frame, data, ax, center_pos, max_distance, areaSize):
    print(f"Frame {frame}/{len(data)}")
    plot_2d(ax, data[frame]['cells'], center_pos, max_distance, areaSize)


def update_3d(frame, data, ax, center_pos, max_distance, areaSize):
    print(f"Frame {frame}/{len(data)}")
    plot_3d(ax, data[frame]['cells'], center_pos, max_distance, areaSize)


def calculate_center(areaSize):
    return areaSize // 2


def calculate_max_distance_2d(center_pos, areaSize):
    corners = [(0, 0), (0, areaSize), (areaSize, 0), (areaSize, areaSize)]
    return max([np.sqrt((x - center_pos[0]) ** 2 + (y - center_pos[1]) ** 2) for x, y in corners])


def calculate_max_distance_3d(center_pos, areaSize):
    corners = [(0, 0, 0), (0, 0, areaSize), (0, areaSize, 0), (areaSize, 0, 0),
               (areaSize, areaSize, 0), (areaSize, 0, areaSize), (0, areaSize, areaSize),
               (areaSize, areaSize, areaSize)]
    return max([np.sqrt((x - center_pos[0]) ** 2 + (y - center_pos[1]) ** 2 + (z - center_pos[2]) ** 2) for x, y, z in
                corners])


def animate(data, static, output_file, is_3d=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') if is_3d else fig.add_subplot(111)
    areaSize = static["areaSize"]
    center_pos = (calculate_center(areaSize), calculate_center(areaSize)) if not is_3d else \
        (calculate_center(areaSize), calculate_center(areaSize), calculate_center(areaSize))

    max_distance = calculate_max_distance_3d(center_pos, areaSize) if is_3d else calculate_max_distance_2d(center_pos,
                                                                                                           areaSize)

    if is_3d:
        ani = animation.FuncAnimation(fig, update_3d, frames=len(data),
                                      fargs=(data, ax, center_pos, max_distance, areaSize))
    else:
        ani = animation.FuncAnimation(fig, update_2d, frames=len(data),
                                      fargs=(data, ax, center_pos, max_distance, areaSize))

    ani.save(output_file, fps=3)
    plt.close(fig)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python animation.py <data.json> <static.json>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    with open(sys.argv[2], 'r') as f:
        static = json.load(f)

    output_file = sys.argv[3] if len(sys.argv) > 3 else 'animation.mp4'

    start_time = time.time()
    # Call the animation function with 2D or 3D
    if static["is3D"]:
        animate(data, static, output_file, is_3d=True)
    else:
        animate(data, static, output_file, is_3d=False)

    print(f"--- Time: {time.time() - start_time} ---")
