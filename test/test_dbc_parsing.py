import cantools
import os
import sys

def parse_dbc(file_path):
    try:
        db = cantools.database.load_file(file_path)
        print(f"Successfully parsed {file_path}")
        for message in db.messages:
            print(f"Message ID: {message.frame_id}, Name: {message.name}")
            for signal in message.signals:
                print(f"  Signal Name: {signal.name}, Start Bit: {signal.start}, Length: {signal.length}")
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_dbc_parsing.py <test|main>")
        sys.exit(1)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    dbc_type = sys.argv[1]
    if dbc_type == 'test':
        dbc_file_path = os.path.join(script_dir, 'data', 'test.dbc')
    elif dbc_type == 'main':
        dbc_file_path = os.path.join(script_dir, '..', 'data', '1200G_CAN-DBC_v01.01.00.dbc')
    else:
        print("Invalid argument. Use 'test' or 'main'.")
        sys.exit(1)
    
    print(f"Parsing DBC: {dbc_file_path}")
    parse_dbc(dbc_file_path)
