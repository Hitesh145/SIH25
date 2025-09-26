import json

# Load original labeled dataset
with open("logs/labeled_dataset.json") as f:
    original = json.load(f)

# Load feedback
with open("logs/feedback_log.json") as f:
    feedback = json.load(f)

# Convert feedback to training format
feedback_data = []
for entry in feedback:
    label = 1 if entry["analyst_decision"] == "suspicious" else 0
    feedback_data.append({
        "text": entry["text"],
        "label": label
    })

# Merge and save
merged = original + feedback_data
with open("logs/updated_dataset.json", "w") as f:
    json.dump(merged, f, indent=2)

print(f"Merged {len(feedback_data)} feedback entries into training set.")