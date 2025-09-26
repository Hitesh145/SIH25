import time
# from live.inference_engine import score_request

# this is used to keep eye on the live requests 
# When a new request is made it acces it and print it on terminal
# It will be used to get live request and check the request for anomoly/malicious request and also used to train the model

def stream_logs(log_path):
    with open(log_path, 'r') as f:
        f.seek(0, 2)  # Move to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            print(line.strip())
            # log_entry = line.strip()
            # score = score_request(log_entry)
            # label = "suspicious" if score > 0.6 else "benign"
            # print(f"[{label.upper()}] {log_entry} → Score: {score:.2f}")


try:
    stream_logs(r'C:\xampp\apache\logs\access.log')
except KeyboardInterrupt:
    print("Stopped log streaming.")
