import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # Load the data
    data_beeman = pd.read_csv('outputBeeman.txt')
    data_verlet = pd.read_csv('outputVerlet.txt')
    data_gear = pd.read_csv('outputGear.txt')

    print(data_beeman)

    # Plot the data
    plt.plot(data_beeman['time'], data_beeman['position'], label='Beeman', marker='o', linestyle='')
    plt.plot(data_verlet['time'], data_verlet['position'], label='Verlet', marker='o', linestyle='')
    plt.plot(data_gear['time'], data_gear['position'], label='Gear', marker='o', linestyle='')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.legend(loc='lower right')
    plt.show()
