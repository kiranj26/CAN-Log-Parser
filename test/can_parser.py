import re
from decimal import Decimal

def read_log_file(file_path):
    can_messages = []
    start_time = None
    end_time = None

    with open(file_path, 'r') as file:
        for line in file:
            if "Safety Processor_toyota_a.UniversalCommand" in line:
                time_match = re.search(r'\d+\.\d+', line)
                if time_match:
                    timestamp = Decimal(time_match.group())
                    if start_time is None:
                        start_time = timestamp
                    end_time = timestamp
                
                message_id = int(line.split()[2], 16)
                message_data = {}
                while True:
                    next_line = next(file).strip()
                    if not next_line.startswith('->'):
                        break
                    parts = next_line.split()
                    signal_name = parts[1]
                    signal_value = float(parts[2])
                    message_data[signal_name] = signal_value
                
                can_messages.append((timestamp, message_id, message_data, "UniversalCommand"))

    return can_messages, start_time, end_time

def decode_signals(can_messages, dbc_file):
    # Assuming dbc decoding logic implemented here
    signal_data = {
        'UC_ControlMode': [],
        'UC_CommandCounter': [],
        'UC_ActiveDischarge': [],
        'UC_UseRawSpeed': [],
        'UCS_DirOfRotation': [],
        'UC_Enable': []
    }
    
    for timestamp, message_id, data, message_name in can_messages:
        for signal in data:
            if signal in signal_data:
                signal_data[signal].append((timestamp, data[signal]))
    
    return signal_data
