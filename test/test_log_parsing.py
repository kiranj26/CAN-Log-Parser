import re

def parse_log_file(log_path):
    with open(log_path, 'r') as file:
        log_data = file.readlines()
    return log_data

if __name__ == "__main__":
    log_path = 'test/data/test_log.txt'
    log_data = parse_log_file(log_path)
    for line in log_data:
        print(line.strip())
