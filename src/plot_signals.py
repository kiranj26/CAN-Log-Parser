import matplotlib.pyplot as plt

def plot_signals(signal_data):
    for signal_name, data in signal_data.items():
        if data:
            timestamps, values = zip(*data)
            plt.figure()
            plt.plot(timestamps, values, label=signal_name)
            plt.title(signal_name)
            plt.xlabel('Time (s)')
            plt.ylabel(signal_name)
            plt.legend()
            plt.show()
