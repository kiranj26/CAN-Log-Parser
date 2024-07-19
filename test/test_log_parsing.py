import cantools
import os
import sys

def parse_dbc(file_path):
    try:
        db = cantools.database.load_file(file_path)
        print(f"Successfully parsed DBC file: {file_path}")
        return db
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def parse_log(db, log_file_path):
    try:
        parsed_data = []
        with open(log_file_path, 'r') as log_file:
            current_message = None
            for line in log_file:
                # print(f"Reading line: {line.strip()}")  # Commented for clean output
                if line.startswith("CAN"):
                    if current_message:
                        process_message(db, current_message, parsed_data)
                    current_message = [line.strip()]
                    # print("Detected start of a new message")  # Commented for clean output
                elif line.strip().startswith("->"):
                    # print("Detected start of line with ->")
                    current_message.append(line.strip())
                    # print(f"Appending signal line: {line.strip()}")  # Commented for clean output
            if current_message:
                process_message(db, current_message, parsed_data)
        print_parsed_data(parsed_data)
    except Exception as e:
        print(f"Error parsing log file {log_file_path}: {e}")

def process_message(db, message_lines, parsed_data):
    try:
        # print(f"Processing message lines: {message_lines}")  # Commented for clean output
        main_line = message_lines[0].split()
        # print(f"Main line parts: {main_line}")  # Commented for clean output
        can_id = main_line[2]
        message_name = main_line[5]
        timestamp = main_line[6]
        direction = main_line[7]

        signals = []

        for signal_line in message_lines[1:]:
            parts = signal_line.split()
            signal_name = parts[1]
            signal_value = parts[2]
            signals.append((signal_name, signal_value, timestamp))

        parsed_data.append({
            "message_name": message_name,
            "can_id": can_id,
            "timestamp": timestamp,
            "direction": direction,
            "signals": signals
        })
        
    except Exception as e:
        print(f"Error processing message: {e}")

def print_parsed_data(parsed_data):
    for data in parsed_data:
        print(f"Message: {data['message_name']}, CAN ID: {data['can_id']}, Timestamp: {data['timestamp']}, Direction: {data['direction']}")
        for signal in data['signals']:
            signal_name, signal_value, signal_timestamp = signal
            print(f"  Signal: {signal_name}, Value: {signal_value}, Timestamp: {signal_timestamp}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_log_parsing.py [test|main]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "test":
        dbc_file = "C:\\Github\\CAN-Log-Parser\\test\\data\\test.dbc"
        log_file = "C:\\Github\\CAN-Log-Parser\\test\\data\\test_log.txt"
    elif mode == "main":
        dbc_file = "C:\\Github\\CAN-Log-Parser\\data\\1200G_CAN-DBC_v01.01.00.dbc"
        log_file = "C:\\Github\\CAN-Log-Parser\\data\\DMW_Message_Timeout_CAN_Log.txt"
    else:
        print("Invalid mode. Use 'test' or 'main'.")
        sys.exit(1)

    db = parse_dbc(dbc_file)
    if db:
        parse_log(db, log_file)
