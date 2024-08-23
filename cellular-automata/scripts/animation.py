import json
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def plot_2d(ax, cells):
    ax.clear()
    for cell in cells:
        color = 'blue' if cell['state'] == 1 else 'green'
        rect = plt.Rectangle((cell['x'], cell['y']), 1, 1, color=color)
        ax.add_patch(rect)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_aspect('equal')

def plot_3d(ax, cells):
    ax.clear()
    for cell in cells:
        color = 'blue' if cell['state'] == 1 else 'green'
        ax.bar3d(cell['x'], cell['y'], cell.get('z', 0), 1, 1, 1, color=color)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_zlim(0, 20)

def update_2d(frame, data, ax):
    plot_2d(ax, data[frame]['cells'])

def update_3d(frame, data, ax):
    plot_3d(ax, data[frame]['cells'])

def animate(data, is_3d=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') if is_3d else fig.add_subplot(111)

    if is_3d:
        ani = animation.FuncAnimation(fig, update_3d, frames=len(data), fargs=(data, ax))
    else:
        ani = animation.FuncAnimation(fig, update_2d, frames=len(data), fargs=(data, ax))

    plt.show()


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    # Call the animation function with 2D or 3D
    # animate(data, is_3d=False)  # 2D animation
    animate(data, is_3d=True)   # 3D animation
