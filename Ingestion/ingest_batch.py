import os

# This will open the log file and take the logs from the given path 

def ingest_logs(log_path):
    with open(log_path, 'r') as f:
        for line in f:
            yield line.strip()

# Example usage
# Currenty prints but can be used to make a log file to get data/logs to train the model

count = 10
for log in ingest_logs(r'C:\xampp\apache\logs\access.log'):
    if count > 0 :
        print(log)