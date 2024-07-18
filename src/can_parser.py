import cantools
import csv

def read_log_file(log_file):
    can_messages = []
    with open(log_file, 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        for row in reader:
            can_id = int(row[1], 16)
            data = bytes.fromhex(row[2])
            timestamp = float(row[0])
            can_messages.append((timestamp, can_id, data))
    return can_messages

def decode_signals(can_messages, dbc_file):
    db = cantools.database.load_file(dbc_file)
    signal_data = {}
    for timestamp, can_id, data in can_messages:
        try:
            message = db.get_message_by_frame_id(can_id)
            decoded_signals = message.decode(data)
            for signal_name, value in decoded_signals.items():
                if signal_name not in signal_data:
                    signal_data[signal_name] = []
                signal_data[signal_name].append((timestamp, value))
        except KeyError:
            continue
    return signal_data
