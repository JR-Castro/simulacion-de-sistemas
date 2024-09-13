import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from read_files import read_static_file, read_dynamic_file, read_output_file, get_all_particles_states


def update_circle(frame, sim_output, ax, static_data):
    print(f"{frame}/{len(sim_output)}")
    ax.clear()

    # Set axis limits and ensure 1:1 aspect ratio
    ax.set_xlim(-static_data['length'] / 2, static_data['length'] / 2)
    ax.set_ylim(-static_data['length'] / 2, static_data['length'] / 2)
    # Ensure 1:1 aspect ratio
    ax.set_aspect('equal', 'box')

    # Draw the boundary of the circle (container)
    ax.add_patch(plt.Circle((0, 0), radius=static_data['length'] / 2, color='black', fill=False, linestyle='--'))

    # Plot particles
    particles = sim_output[frame]['particles']
    for p in particles:
        # Particle position and velocity
        x, y = p[1], p[2]
        vx, vy = p[3], p[4]

        # Particle radius from static data
        radius = static_data['particles'][p[0]-1][1]

        # Calculate speed
        speed = np.sqrt(vx**2 + vy**2)

        # Scale the velocity vector so that when speed = 1, the line has the length of the radius
        if speed != 0:
            line_length = radius * speed
            vx_scaled = vx / speed * line_length
            vy_scaled = vy / speed * line_length
        else:
            vx_scaled = vy_scaled = 0  # No velocity, no line

        # Draw particle
        if p[0] == 1:
            # Draw particle 1 in red with fill
            ax.add_patch(plt.Circle((x, y), radius=radius, color='red', fill=True))
        else:
            # Draw other particles with no fill, only circle outlines
            ax.add_patch(plt.Circle((x, y), radius=radius, edgecolor='blue', fill=False))

        # Draw the velocity vector (black line)
        ax.plot([x, x + vx_scaled], [y, y + vy_scaled], color='black', linewidth=0.5)
    return ax

def update_square(frame, sim_output, ax, static_data):


    return ax

def animate(sim_output, static_data, output_file):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # sim_output = sim_output[:10]

    if static_data['container'] == 'CIRCLE':
        ani = animation.FuncAnimation(fig, update_circle, frames=len(sim_output), fargs=(sim_output, ax, static_data))
    else:
        ani = animation.FuncAnimation(fig, update_square, frames=len(sim_output), fargs=(sim_output, ax, static_data))

    ani.save(output_file, fps=4, dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python generate_animation.py <static_file> <dynamic_file> <output_file> <dt>")
        sys.exit(1)

    static_file = sys.argv[1]
    dynamic_file = sys.argv[2]
    output_file = sys.argv[3]
    dt = float(sys.argv[4])

    output_animation_file = sys.argv[5] if len(sys.argv) > 5 else 'output'

    static_data = read_static_file(static_file)
    dynamic_data = read_dynamic_file(static_data, dynamic_file)
    sim_output = read_output_file(output_file, dt)
    sim_output.insert(0, {'time': 0, 'particles': dynamic_data})
    full_states = get_all_particles_states(sim_output)


    animate(full_states, static_data, output_animation_file)