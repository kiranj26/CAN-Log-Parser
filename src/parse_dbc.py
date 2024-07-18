import cantools

# Load the DBC file
dbc_file_path = '../data/1200G_CAN-DBC_v01.01.00.dbc'
db = cantools.database.load_file(dbc_file_path)

# List all messages and signals in the DBC file
dbc_messages = db.messages
messages_signals = {msg.name: [signal.name for signal in msg.signals] for msg in dbc_messages}

# Display the messages and their signals
for message, signals in messages_signals.items():
    print(f"Message: {message}")
    for signal in signals:
        print(f"  Signal: {signal}")
