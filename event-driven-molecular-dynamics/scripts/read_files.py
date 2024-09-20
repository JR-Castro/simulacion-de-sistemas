def read_static_file(file_path):
    """
    Returns a dictionary with the static information of the simulation
    :param file_path: str
    :return: { container: str, length: float, N: int, time: float, particles: List[(p_num: int, p_radius: float, p_mass: float)] }
    """
    static = {}
    with open(file_path, 'r') as f:
        static["container"] = f.readline().strip()
        static["length"] = float(f.readline())
        static["N"] = int(f.readline())
        static["time"] = float(f.readline())
        static["outputStep"] = float(f.readline())

        particles = []
        for i in range(static["N"]):
            particle_attr = f.readline().split(" ")

            p_num = int(particle_attr[0])
            p_radius = float(particle_attr[1])
            p_mass = float(particle_attr[2])

            particles.append((p_num, p_radius, p_mass))

        static["particles"] = particles

    return static


def read_dynamic_file(static, file_path):
    """
    Returns the first state of the system
    :param static: dict
    :param file_path: str
    :return: List[(p_num: int, x: float, y: float, vx: float, vy: float)]
    """
    dynamic = []
    with open(file_path, 'r') as f:
        f.readline()
        for i in range(static["N"]):
            dynamic.append(read_output_particle(f.readline()))

    return dynamic


def get_all_particles_states(sim_output):
    states = [sim_output[0]]

    last_particles = sim_output[0]['particles']

    for state in sim_output[1:]:
        time = state['time']
        particles = state['particles']

        full_state = list(last_particles)

        for p in particles:
            full_state[p[0]-1] = p

        states.append({'time': time, 'particles': full_state})
        last_particles = full_state

    return states


def read_collisions(file_path):
    output = []
    with open(file_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            coll_time, coll_particles = read_output_collision_info(line)
            particles = [read_output_particle(f.readline())]
            if coll_particles == 2:
                particles.append(read_output_particle(f.readline()))
            output.append({'time': coll_time, 'particles': particles})

    return output


def read_collisions_with_obstacle(file_path):
    count = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.rstrip().endswith(" 1"):
                count += 1
    return count


def read_unique_collisions_with_obstacle(file_path):
    count = 0
    previous_first_words = set()

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for i in range(len(lines) - 1):
            current_line = lines[i].rstrip()  # Remove trailing whitespace
            next_line = lines[i + 1].rstrip()

            # Check if the current line ends with " 1"
            if current_line.endswith(" 1"):
                # Get the first word of the next line
                next_first_word = next_line.split()[0] if next_line else ''

                # If the first word is distinct, count it
                if next_first_word not in previous_first_words:
                    count += 1
                    if count >= 200:
                        return float(current_line.split()[0])
                    previous_first_words.add(next_first_word)

    return 1.0


def read_collisions_discrete_steps(file_path, dt, avoid_repeats=True):
    """
    Returns a list of dictionaries with the status of the system at each time step
    :param file_path: str
    :param dt: float
    :return: List[{ time: float, particles: List[(p_num: int, x: float, y: float, vx: float, vy: float)] }]
    """
    time = 0
    sim_output = []
    with open(file_path, 'r') as f:

        time_state = {}
        particles = []
        time_state['time'] = time

        while True:
            line = f.readline()
            if not line:
                time_state['particles'] = particles
                sim_output.append(time_state)
                break
            coll_time, coll_particles = read_output_collision_info(line)
            if coll_time >= time + dt:
                time_state['particles'] = particles
                sim_output.append(time_state)
                time = time + dt
                time_state = {}
                particles = []
                time_state['time'] = time
                time_state['particles'] = particles

            particle = read_output_particle(f.readline())

            # Prevent same particle from having different states in same time step
            if avoid_repeats:
                particles = [p for p in particles if p[0] != particle[0]]

            particles.append(particle)
            if coll_particles == 2:
                particle = read_output_particle(f.readline())
                particles = [p for p in particles if p[0] != particle[0]]
                particles.append(particle)

        time_state['particles'] = particles

    return sim_output


def read_states_output_file(static_data, file_path):
    """
    Returns a list of dictionaries with the whole status of the system at each time step
    :param static_data: Static data
    :param file_path: str
    :return: List[{ time: float, particles: List[(p_num: int, x: float, y: float, vx: float, vy: float)] }]
    """
    sim_output = []
    with open(file_path, 'r') as f:

        while True:
            particles = []
            line = f.readline()
            if line is None or line.strip() == '':
                break
            time = float(line)

            for i in range(static_data['N']):
                particles.append(read_output_particle(f.readline()))

            sim_output.append({'time': time, 'particles': particles})

    return sim_output


def read_output_collision_info(line: str):
    collision_info = line.split(" ")
    return float(collision_info[0]), int(collision_info[1])


def read_output_particle(line: str):
    p_attr = line.split(' ')

    p_num = int(p_attr[0])
    p_x = float(p_attr[1])
    p_y = float(p_attr[2])
    p_vx = float(p_attr[3])
    p_vy = float(p_attr[4])

    return p_num, p_x, p_y, p_vx, p_vy
