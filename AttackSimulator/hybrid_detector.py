import json

# Load anomaly scores and classifier predictions
with open("scored_logs.json") as f:
    logs = json.load(f)

with open("classifier_outputs.json") as f:
    predictions = json.load(f)

# Combine scores
hybrid = []
if len(logs) != len(predictions):
    raise ValueError("Mismatch between logs and predictions length")

for log, pred in zip(logs, predictions):
    final_score = 0.6 * pred["prob_attack"] + 0.4 * log["anomaly_score"]
    hybrid.append({
        "text": log["flat_text"],
        "final_score": final_score,
        "label": "suspicious" if final_score > 0.6 else "benign"
    })

with open("hybrid_scores.json", "w") as f:
    json.dump(hybrid, f, indent=2)

print("Hybrid detection complete.")