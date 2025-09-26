from transformers import AutoTokenizer, AutoModel
import torch
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import time

# ✅ Use a faster model
MODEL_NAME = "distilbert-base-uncased"

# ✅ GPU support
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).to(device)

# ✅ Flatten structured logs
def flatten_log(entry):
    parts = [entry["method"], entry["path"]]
    for k, v in entry.get("normalized_query", {}).items():
        parts.append(f"{k}={v}")
    return " ".join(parts)

# ✅ Batched embedding function
def embed_batch(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].cpu().numpy()  # CLS token

# ✅ Load or compute benign centroid
centroid_path = "states/benign_centroid.npy"
if os.path.exists(centroid_path):
    centroid = np.load(centroid_path)
    print("✅ Loaded cached centroid")
else:
    with open("logs/benign_logs.json") as f:
        benign = json.load(f)
        benign = benign[:100]
    benign_texts = [flatten_log(entry) for entry in benign]
    benign_embeddings = embed_batch(benign_texts)
    centroid = np.mean(benign_embeddings, axis=0)
    np.save(centroid_path, centroid)
    print("✅ Computed and cached centroid")

# ✅ Score new logs
with open("logs/tokenized_logs.json") as f:
    logs = json.load(f)

texts = [entry["flat_text"] for entry in logs]
embeddings = embed_batch(texts)

scored = []
for entry, emb in zip(logs, embeddings):
    score = cosine_similarity([emb], [centroid])[0][0]
    anomaly_score = float(1 - score)
    scored.append({**entry, "anomaly_score": anomaly_score})

# ✅ Save results
os.makedirs("logs", exist_ok=True)
with open("logs/scored_logs.json", "w") as f:
    json.dump(scored, f, indent=2)

print("🚀 Anomaly scoring complete.")
