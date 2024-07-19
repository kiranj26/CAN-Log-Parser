import cantools
import sys
import os
import matplotlib.pyplot as plt
import argparse

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
        return parsed_data
    except Exception as e:
        print(f"Error parsing log file {log_file_path}: {e}")
        return None

def process_message(db, message_lines, parsed_data):
    try:
        # print(f"Processing message lines: {message_lines}")  # Commented for clean output
        main_line = message_lines[0].split()
        # print(f"Main line parts: {main_line}")  # Commented for clean output
        can_id = main_line[2]
        # if can_id in ["00000000", "0000040A"]:
        #     return
        ecu_name, message_name = main_line[6].split('.')
        timestamp = main_line[7]
        direction = main_line[8]

        signals = []

        for signal_line in message_lines[1:]:
            # print("Signal Line ---- ", signal_line)
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
        print(f"Error processing message: {e}, for CAN ID (Error Frames): {can_id}")
        return

def print_parsed_data(parsed_data):
    for data in parsed_data:
        #print(f"Message: {data['message_name']}, CAN ID: {data['can_id']}, Timestamp: {data['timestamp']}, Direction: {data['direction']}")
        for signal in data['signals']:
            signal_name, signal_value, signal_timestamp = signal
            #print(f"  Signal: {signal_name}, Value: {signal_value}, Timestamp: {signal_timestamp}")


def plot_signals(parsed_data, signal_name, start_time, end_time):
    timestamps = []
    values = []
    for data in parsed_data:
        for signal in data['signals']:
            s_name, s_value, s_timestamp = signal
            try:
                s_value = float(s_value)
                s_timestamp = float(s_timestamp) / 1000  # Convert timestamp to seconds here
            except ValueError as e:
                print(f"Error converting value: {e}")
                continue

            if s_name == signal_name and (start_time is None or s_timestamp >= start_time) and (end_time is None or s_timestamp <= end_time):
                timestamps.append(s_timestamp)
                values.append(s_value)

    if not timestamps:
        print(f"No data found for signal: {signal_name}")
        return

    plt.figure(figsize=(15, 5))  # Adjust the size as needed
    plt.plot(timestamps, values)
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title(f'Signal: {signal_name}')
    plt.grid(True)

    # Format the x-axis to display timestamps correctly in seconds
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot CAN signal data")
    parser.add_argument('mode', choices=['test', 'main'], help="Mode to run the script in")
    parser.add_argument('signal', type=str, help="Signal name to plot")
    parser.add_argument('start', type=float, nargs='?', default=None, help="Start time for the plot")
    parser.add_argument('end', type=float, nargs='?', default=None, help="End time for the plot")

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    dbc_file = os.path.join(script_dir, "..", "data", "test.dbc")
    log_file = os.path.join(script_dir, "..", "data", "test_log.txt")

    db = parse_dbc(dbc_file)
    if db:
        parsed_data = parse_log(db, log_file)
        if parsed_data:
            if args.start is None or args.end is None:
                all_timestamps = [float(data['timestamp']) / 1000 for data in parsed_data for signal in data['signals']]
                start_time = min(all_timestamps) if args.start is None else args.start
                end_time = max(all_timestamps) if args.end is None else args.end
            else:
                start_time = args.start
                end_time = args.end
            plot_signals(parsed_data, args.signal, start_time, end_time)
        else:
            print("Parsed data is empty or None.")
    else:
        print("DBC parsing failed.")