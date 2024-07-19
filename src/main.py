import cantools
import sys
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
                if line.startswith("CAN"):
                    if current_message:
                        process_message(db, current_message, parsed_data)
                    current_message = [line.strip()]
                elif line.strip().startswith("->"):
                    current_message.append(line.strip())
            if current_message:
                process_message(db, current_message, parsed_data)
        return parsed_data
    except Exception as e:
        print(f"Error parsing log file {log_file_path}: {e}")
        return None

def process_message(db, message_lines, parsed_data):
    try:
        main_line = message_lines[0].split()
        can_id = int(main_line[2], 16)
        message_name = main_line[5]
        timestamp = float(main_line[6])
        direction = main_line[7]

        signals = []

        for signal_line in message_lines[1:]:
            parts = signal_line.split()
            signal_name = parts[1]
            signal_value = float(parts[2])
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

def plot_signals(parsed_data, signal_name, start_time, end_time):
    timestamps = []
    values = []
    for data in parsed_data:
        for signal in data['signals']:
            s_name, s_value, s_timestamp = signal
            if s_name == signal_name and (start_time is None or s_timestamp >= start_time) and (end_time is None or s_timestamp <= end_time):
                timestamps.append(s_timestamp)
                values.append(s_value)

    if not timestamps:
        print(f"No data found for signal: {signal_name}")
        return

    plt.figure()
    plt.plot(timestamps, values, marker='o')
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title(f'Signal: {signal_name}')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot CAN signal data")
    parser.add_argument('mode', choices=['test', 'main'], help="Mode to run the script in")
    parser.add_argument('signal', type=str, help="Signal name to plot")
    parser.add_argument('start', type=float, nargs='?', default=None, help="Start time for the plot")
    parser.add_argument('end', type=float, nargs='?', default=None, help="End time for the plot")

    args = parser.parse_args()

    if args.mode == "test":
        dbc_file = "C:\\Github\\CAN-Log-Parser\\test\\data\\test.dbc"
        log_file = "C:\\Github\\CAN-Log-Parser\\test\\data\\test_log.txt"
    elif args.mode == "main":
        dbc_file = "C:\\Github\\CAN-Log-Parser\\data\\1200G_CAN-DBC_v01.01.00.dbc"
        log_file = "C:\\Github\\CAN-Log-Parser\\data\\DMW_Message_Timeout_CAN_Log.txt"

    db = parse_dbc(dbc_file)
    if db:
        parsed_data = parse_log(db, log_file)
        if parsed_data:
            print("Done parsing log file")
            if args.start is None or args.end is None:
                # Determine the start and end times from the log if not provided
                all_timestamps = [data['timestamp'] for data in parsed_data]
                start_time = min(all_timestamps) if args.start is None else args.start
                end_time = max(all_timestamps) if args.end is None else args.end
            else:
                start_time = args.start
                end_time = args.end

            plot_signals(parsed_data, args.signal, start_time, end_time)
