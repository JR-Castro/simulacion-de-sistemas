import sys
from random import uniform, getrandbits

PARTICLE_RADIUS = 0.001
PARTICLE_MASS = 1

def generate_particle(p_num, layout, L, p_radius, p_mass, speed_module):
    speed_x = uniform(-speed_module, speed_module)
    speed_y = (speed_module - speed_x ** 2) ** 0.5
    if bool(getrandbits(1)):
        speed_y *= -1

    if (speed_x ** 2 + speed_y ** 2) ** 0.5 > speed_module ** 2:
        print('something went wrong')
        sys.exit(1)


    if layout == 'SQUARE':
        x = uniform(-L/2 + p_radius, L/2 - p_radius)
        y = uniform(-L/2 + p_radius, L/2 + p_radius)
        return p_num, x, y, p_radius, p_mass, speed_x, speed_y

    r = L / 2
    x = uniform(-r + p_radius, r - p_radius)
    y = uniform(-r + p_radius, r - p_radius)
    while x ** 2 + y ** 2 > (r - p_radius) ** 2:
        x = uniform(-r + p_radius, r - p_radius)
        y = uniform(-r + p_radius, r - p_radius)
    return p_num, x, y, p_radius, p_mass, speed_x, speed_y


def check_particle_collision(particles, particle):
    if len([p for p in particles if
            (p[1] - particle[1]) ** 2 + (p[2] - particle[2]) ** 2 < (p[3] + particle[3]) ** 2]) > 0:
        return True
    return False


def generate_particles(particles: list, layout, L, N, speed_module):
    for i in range(len(particles) + 1, N + 1):
        new_particle = generate_particle(i, layout, L, PARTICLE_RADIUS, PARTICLE_MASS, speed_module)
        while check_particle_collision(particles, new_particle):
            new_particle = generate_particle(i, layout, L, PARTICLE_RADIUS, PARTICLE_MASS, speed_module)
        particles.append(new_particle)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(
            'Usage: python generate_static.py <output_file> <dynamic_amount> <layout> <L> <N> <T> <speed_module> [Obstacle_radius Obstacle_mass]')
        sys.exit(1)

    output_file = sys.argv[1]
    dynamic_amount = int(sys.argv[2])
    layout = sys.argv[3]
    L = float(sys.argv[4])
    N = int(sys.argv[5])
    T = float(sys.argv[6])
    speed_module = float(sys.argv[7])

    particles = []
    if len(sys.argv) == 10:
        obstacle_radius = float(sys.argv[8])
        obstacle_mass = float(sys.argv[9])
        particles.append((1, 0, 0, obstacle_radius, obstacle_mass, 0, 0))

    if L <= 0 or N <= 0 or T <= 0 or speed_module <= 0:
        print('Invalid input')
        sys.exit(1)
    if not ('SQUARE' == layout or 'CIRCLE' == layout):
        print('Invalid layout')
        sys.exit(1)

    generate_particles(particles, layout, L, N, speed_module)

    output_file_parts = output_file.split('.')

    with open(''.join(output_file_parts[:-1]) + '.' + output_file_parts[-1], 'w') as f:
        f.write(layout)
        f.write('\n')
        f.write(str(L))
        f.write('\n')
        f.write(str(N))
        f.write('\n')
        f.write(str(T))
        f.write('\n')
        f.write('0.1\n')
        for i, particle in enumerate(particles):
            p_num, x, y, p_radius, p_mass, speed_x, speed_y = particle
            f.write(' '.join(map(str, [p_num, p_radius, p_mass])))
            if i < len(particles) - 1:
                f.write('\n')

    for i in range(dynamic_amount):
        with open(''.join(output_file_parts[:-1]) + f'_{i}.' + output_file_parts[-1], 'w') as f:
            f.write('0')
            f.write('\n')
            for i, particle in enumerate(particles):
                p_num, x, y, p_radius, p_mass, speed_x, speed_y = particle
                f.write(' '.join(map(str, [p_num, x, y, speed_x, speed_y])))
                if i < len(particles) - 1:
                    f.write('\n')
        particles = particles[:1]
        generate_particles(particles, layout, L, N, speed_module)
