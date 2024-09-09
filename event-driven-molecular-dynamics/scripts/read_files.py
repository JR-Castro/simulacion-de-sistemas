def read_static_file(file_path):
    """
    Returns a dictionary with the static information of the simulation
    :param file_path: str
    :return: { container: float, length: float, N: int, time: float, particles: List[(p_num: int, p_radius: float, p_mass: float)] }
    """
    static = {}
    with open(file_path, 'r') as f:
        static["container"] = f.readline()
        static["length"] = float(f.readline())
        static["N"] = int(f.readline())
        static["time"] = float(f.readline())

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


def read_output_file(file_path, dt):
    """
    Returns a list of dictionaries with the status of the system at each time step
    :param file_path: str
    :param dt: float
    :return: List[{ time: float, particles: List[(p_num: int, x: float, y: float, vx: float, vy: float)] }]
    """
    time = 0
    status = []
    with open(file_path, 'r') as f:

        time_state = {}
        particles = []
        time_state['time'] = time
        time_state['particles'] = particles

        while True:
            line = f.readline()
            if not line:
                status.append(time_state)
                break
            coll_time, coll_particles = read_output_collision_info(line)
            if coll_time >= time + dt:
                status.append(time_state)
                time = time + dt
                time_state = {}
                particles = []
                time_state['time'] = time
                time_state['particles'] = particles

            particles.append(read_output_particle(f.readline()))
            if coll_particles > 2:
                particles.append(read_output_particle(f.readline()))

    return status


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
