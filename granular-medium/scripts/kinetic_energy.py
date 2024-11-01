import time
import matplotlib.pyplot as plt
import pandas as pd

from animation import N, W, L

if __name__ == '__main__':
    start_time = time.time()

    MASS = 1.0

    data = pd.read_csv("outputs/dynamicData_states.csv")

    frames = int(len(data['time'])/N)
    for i in range(frames):
        frame_data = data.iloc[i * N:(i + 1) * N, :]
        for row in frame_data.itertuples():
            if not (-1 <= row.x <= L + 1 and -1 <= row.y <= W + 1):
                print(f"Particle {row.Index % N} is out of bounds at ({row.x}, {row.y})")

    # Calculate kinetic energy for each particle at each time step
    data['kinetic_energy'] = 0.5 * MASS * (data['vx'] ** 2 + data['vy'] ** 2)

    # Sum kinetic energy for each time step
    kinetic_energy_vs_time = data.groupby('time')['kinetic_energy'].sum()

    # Plot kinetic energy vs time
    plt.figure(figsize=(10, 6))
    plt.plot(kinetic_energy_vs_time.index, kinetic_energy_vs_time.values, label='Total Kinetic Energy')
    plt.xlabel('Time')
    plt.ylabel('Total Kinetic Energy')
    plt.ylim(0, 1000)
    # Log y axis
    # plt.yscale('log')
    plt.title('Kinetic Energy of the System vs Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    print(f"Elapsed time: {time.time() - start_time:.2f}s")
