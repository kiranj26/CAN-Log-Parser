"""
/**
 * @file main.py
 * @brief Script to parse CAN DBC files and log files, and plot specific CAN signal data over time.
 *
 * This script is designed to parse a DBC file to understand the structure of CAN messages and a log file
 * to extract actual CAN message data. It then plots the specified signal data over time.
 *
 * The script uses the `cantools` library to parse the DBC file and understand the CAN message structure.
 * The log file is parsed to extract individual CAN messages and their signals, which are then plotted using `matplotlib`.
 *
 *
 * The script is designed to work with relative paths, making it easy to clone the repository and run the script without modifying paths.
 *
 * Author: Kiran Jojare
 *
 * Usage:
 *   python main.py <test|main> <signal_name> [start_time] [end_time]
 *
 * Arguments:
 *   mode: Mode to run the script in ('test' or 'main')
 *   signal: Signal name to plot
 *   start: (Optional) Start time for the plot
 *   end: (Optional) End time for the plot
 */
"""

import cantools
import os
import sys
import matplotlib.pyplot as plt
import argparse

def parse_dbc(file_path):
    """
    @brief Parse the DBC file to get CAN message definitions.
    
    @param file_path Path to the DBC file.
    @return Parsed DBC database object.
    """
    try:
        db = cantools.database.load_file(file_path)
        print(f"Successfully parsed DBC file: {file_path}")
        return db
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def parse_log(db, log_file_path):
    """
    @brief Parse the log file to extract CAN messages.
    
    @param db Parsed DBC database object.
    @param log_file_path Path to the log file.
    @return List of parsed CAN messages.
    """
    try:
        parsed_data = []
        with open(log_file_path, 'r') as log_file:
            current_message = None
            for line in log_file:
                # print(f"Reading line: {line.strip()}")  # Debug print
                if line.startswith("CAN"):
                    if current_message:
                        process_message(db, current_message, parsed_data)
                    current_message = [line.strip()]
                    # print("Detected start of a new message")  # Debug print
                elif line.strip().startswith("->"):
                    # print("Detected start of line with ->")  # Debug print
                    current_message.append(line.strip())
                    # print(f"Appending signal line: {line.strip()}")  # Debug print
            if current_message:
                process_message(db, current_message, parsed_data)
        print_parsed_data(parsed_data)
        return parsed_data
    except Exception as e:
        print(f"Error parsing log file {log_file_path}: {e}")
        return None

def process_message(db, message_lines, parsed_data):
    """
    @brief Process a single CAN message from the log file.
    
    @param db Parsed DBC database object.
    @param message_lines List of lines representing a single CAN message.
    @param parsed_data List to append the parsed message data.
    """
    try:
        # print(f"Processing message lines: {message_lines}")  # Debug print
        main_line = message_lines[0].split()
        # print(f"Main line parts: {main_line}")  # Debug print
        can_id = main_line[2]
        ecu_name, message_name = main_line[6].split('.')
        timestamp = main_line[7]
        direction = main_line[8]

        signals = []

        for signal_line in message_lines[1:]:
            # print("Signal Line ---- ", signal_line)  # Debug print
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
        print(f"Error processing message: {e}, for CAN ID: {can_id}")
        return

def print_parsed_data(parsed_data):
    """
    @brief Print parsed data for debugging purposes.
    
    @param parsed_data List of parsed CAN messages.
    """
    for data in parsed_data:
        #print(f"Message: {data['message_name']}, CAN ID: {data['can_id']}, Timestamp: {data['timestamp']}, Direction: {data['direction']}")
        for signal in data['signals']:
            signal_name, signal_value, signal_timestamp = signal
            #print(f"  Signal: {signal_name}, Value: {signal_value}, Timestamp: {signal_timestamp}")

def plot_signals(parsed_data, signal_name, start_time, end_time):
    """
    @brief Plot the signal data over time.
    
    @param parsed_data List of parsed CAN messages.
    @param signal_name Name of the signal to plot.
    @param start_time Start time for the plot.
    @param end_time End time for the plot.
    """
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

    plt.figure(figsize=(30, 15))  # Adjust the size as needed
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

    # Determine the paths to the DBC and log files based on the mode
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dbc_file = os.path.join(script_dir, "..", "data", "test.dbc")
    log_file = os.path.join(script_dir, "..", "data", "test_log.txt")

    # Parse the DBC file
    db = parse_dbc(dbc_file)
    if db:
        # Parse the log file
        parsed_data = parse_log(db, log_file)
        if parsed_data:
            # Determine start and end times for the plot if not provided
            if args.start is None or args.end is None:
                all_timestamps = [float(data['timestamp']) / 1000 for data in parsed_data for signal in data['signals']]
                start_time = min(all_timestamps) if args.start is None else args.start
                end_time = max(all_timestamps) if args.end is None else args.end
            else:
                start_time = args.start
                end_time = args.end
            # Plot the signals
            plot_signals(parsed_data, args.signal, start_time, end_time)
        else:
            print("Parsed data is empty or None.")
    else:
        print("DBC parsing failed.")
