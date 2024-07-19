import cantools
import re
import matplotlib.pyplot as plt

def parse_dbc_file(dbc_path):
    db = cantools.database.load_file(dbc_path)
    return db

def parse_log_file(log_path):
    with open(log_path, 'r') as file:
        log_data = file.readlines()
    return log_data

def decode_signals(db, log_data):
    signals = []
    for line in log_data:
        match = re.match(r'.*?(\w+)\s+(\w+)\s+\d+\s+(.*?)\s+(\d+\.\d+)\s+\w\s+->\s+(.*?)\s+(\d+\.?\d*)\s+.*', line)
        if match:
            message_id = int(match.group(2), 16)
            timestamp = float(match.group(4))
            signal_name = match.group(5)
            signal_value = float(match.group(6))
            if message_id in db.messages:
                message = db.get_message_by_frame_id(message_id)
                decoded = {signal.name: signal_value for signal in message.signals}
                signals.append((timestamp, signal_name, decoded))
    return signals

def plot_signals(signals):
    timestamps, signal_names, values = zip(*signals)
    signal_data = {}
    
    for timestamp, signal_name, decoded in signals:
        if signal_name not in signal_data:
            signal_data[signal_name] = ([], [])
        signal_data[signal_name][0].append(timestamp)
        signal_data[signal_name][1].append(decoded[signal_name])

    for signal_name, (times, vals) in signal_data.items():
        plt.figure()
        plt.plot(times, vals, label=signal_name)
        plt.xlabel('Time (s)')
        plt.ylabel(signal_name)
        plt.title(f"Signal: {signal_name} Over Time")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    dbc_path = 'test/data/test.dbc'
    log_path = 'test/data/test_log.txt'
    db = parse_dbc_file(dbc_path)
    log_data = parse_log_file(log_path)
    decoded_signals = decode_signals(db, log_data)
    plot_signals(decoded_signals)
