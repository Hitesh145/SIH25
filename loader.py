import json
from datasets import load_dataset

# Load dataset
dataset = load_dataset("muneeburrahman/ai-waf-dataset")
entries = dataset["train"]

# Convert to list of dictionaries
data_list = entries.to_list()

# Save to JSON
with open("logs/labeled_dataset.json", "w") as f:
    json.dump(data_list, f, indent=2)

print("✅ Dataset saved to labeled_dataset.json")