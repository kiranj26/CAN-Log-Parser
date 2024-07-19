import cantools
import re

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

if __name__ == "__main__":
    dbc_path = 'test/data/test.dbc'
    log_path = 'test/data/test_log.txt'
    db = parse_dbc_file(dbc_path)
    log_data = parse_log_file(log_path)
    decoded_signals = decode_signals(db, log_data)
    for signal in decoded_signals:
        print(signal)
