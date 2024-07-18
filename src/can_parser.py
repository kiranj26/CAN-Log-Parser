import re
import cantools

def read_log_file(log_file):
    can_messages = []
    start_time = None
    end_time = None

    with open(log_file, 'r') as file:
        for line in file:
            match = re.match(r'CAN\s+\d+\s+([0-9A-F]+)\s+\w\s+\d+\s+Safety Processor_toyota_a\.(\S+)\s+(\d+\.\d+)', line)
            if match:
                can_id = int(match.group(1), 16)
                message_name = match.group(2)
                timestamp = float(match.group(3))
                if start_time is None:
                    start_time = timestamp
                end_time = timestamp
                signals = {}
                while True:
                    next_line = next(file, None)
                    if next_line is None or not next_line.strip().startswith('->'):
                        break
                    signal_match = re.match(r'->\s+(\S+)\s+(\S+)\s+(\S+)', next_line.strip())
                    if signal_match:
                        signal_name = signal_match.group(1)
                        value = float(signal_match.group(2))
                        signals[signal_name] = value
                can_messages.append((timestamp, can_id, signals, message_name))

    return can_messages, start_time, end_time

def decode_signals(can_messages, dbc_file):
    db = cantools.database.load_file(dbc_file)
    signal_data = {}
    for timestamp, can_id, signals, message_name in can_messages:
        try:
            message = db.get_message_by_frame_id(can_id)
            for signal_name, value in signals.items():
                if signal_name not in signal_data:
                    signal_data[signal_name] = []
                signal_data[signal_name].append((timestamp, value))
        except KeyError:
            continue
    return signal_data
