import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # Load the data
    data = pd.read_csv('output.txt')

    print(data)

    # Plot the data
    plt.plot(data['time'], data['position'], marker='o', linestyle='')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.show()
