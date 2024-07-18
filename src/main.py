from can_parser import read_log_file, decode_signals
from plot_signals import plot_signals

def main():
    dbc_file = 'data/your_dbc_file.dbc'
    log_file = 'data/your_log_file.txt'
    
    can_messages = read_log_file(log_file)
    signal_data = decode_signals(can_messages, dbc_file)
    plot_signals(signal_data)

if __name__ == '__main__':
    main()
