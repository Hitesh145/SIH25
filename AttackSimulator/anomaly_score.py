from transformers import BertTokenizer, BertModel
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load transformer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def embed(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()  # CLS token

# Load benign logs
with open("logs/benign_logs.json") as f:
    benign = json.load(f)

benign_embeddings = np.array([embed(entry["text"])[0] for entry in benign])
centroid = np.mean(benign_embeddings, axis=0)

# Score new logs
with open("log/tokenized_logs.json") as f:
    logs = json.load(f)

scored = []
for entry in logs:
    emb = embed(entry["flat_text"])[0]
    score = cosine_similarity([emb], [centroid])[0][0]
    anomaly_score = 1 - score  # Higher = more anomalous
    scored.append({**entry, "anomaly_score": anomaly_score})

with open("scored_logs.json", "w") as f:
    json.dump(scored, f, indent=2)

print("Anomaly scoring complete.")
