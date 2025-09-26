import time
import json
from inference_engine import score_request
import os

def tail_log(path):
    with open(path, "r") as f:
        f.seek(0, 2)  # Move to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()

os.makedirs("logs", exist_ok=True)
output = []

for log_entry in tail_log("logs/access.log"):
    score = score_request(log_entry)
    label = "suspicious" if score > 0.6 else "benign"
    result = {
        "text": log_entry,
        "score": round(score, 3),
        "label": label
    }
    output.append(result)
    print(f"[{label.upper()}] {log_entry} → Score: {score:.2f}")

    with open("logs/live_scores.json", "w") as f:
        json.dump(output, f, indent=2)