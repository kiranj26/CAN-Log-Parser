from can_parser import read_log_file, decode_signals
from plot_signals import plot_signals

def main():
    dbc_file = '../data/1200G_CAN-DBC_v01.01.00.dbc'
    log_file = '../data/DMW_Message_Timeout_CAN_Log.txt'

    can_messages, start_time, end_time = read_log_file(log_file)
    print(f"Start time: {start_time}")
    print(f"End time: {end_time}")
    
    signal_data = decode_signals(can_messages, dbc_file)

    plot_signals(signal_data)

if __name__ == '__main__':
    main()
