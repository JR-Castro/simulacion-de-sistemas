import pandas as pd
import matplotlib.pyplot as plt

N = 100
FONT = {'family': 'serif',
        'color': 'black',
        'weight': 'normal',
        'size': 14}

if __name__ == '__main__':
    runs = range(0, 9)
    files = [f'output/coupled_oscillator_w{i}.csv' for i in runs]

    wValues = [9.0 + i * 0.25 for i in runs]
    amplitude = []
    i = 0
    for file in files:
        df = pd.read_csv(file)

        frames = int(len(df['time'])/N)
        amplitudes = [df.iloc[i * N:(i+1)*N,:]['position'].max() for i in range(frames)]

        plt.plot(range(frames), amplitudes)
        plt.xlabel('Frame', fontdict=FONT)
        plt.ylabel('Amplitude (m)', fontdict=FONT)
        plt.savefig(f'amplitude_analysis_{i}.png', dpi=300)
        plt.clf()
        i+=1

        amplitude.append(df['position'].max())

    plt.plot(wValues, amplitude, 'o-')


    plt.xlabel('w (rad/s)', fontdict=FONT)
    plt.ylabel('Amplitude (m)', fontdict=FONT)


    plt.savefig('amplitude_analysis.png', dpi=300)

