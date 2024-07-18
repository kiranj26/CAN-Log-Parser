import matplotlib.pyplot as plt

def plot_signals(signal_data):
    for signal_name, data in signal_data.items():
        timestamps, values = zip(*data)
        plt.figure()
        plt.plot(timestamps, values)
        plt.title(signal_name)
        plt.xlabel('Time (s)')
        plt.ylabel(signal_name)
        plt.show()
