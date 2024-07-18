from can_parser import read_log_file, decode_signals
from plot_signals import plot_signals

def main():
    dbc_file = 'data/test_dbc.dbc'
    log_file = 'data/test_log.txt'

    can_messages, start_time, end_time = read_log_file(log_file)
    print(f"Start time: {start_time}")
    print(f"End time: {end_time}")
    
    signal_data = decode_signals(can_messages, dbc_file)
    plot_signals(signal_data)

if __name__ == '__main__':
    main()
