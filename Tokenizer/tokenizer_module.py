import json
from transformers import AutoTokenizer

# Load a pretrained tokenizer (you can swap with RoBERTa, DistilBERT, etc.)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def flatten_log(entry):
    """
    Convert structured log entry into a flat string for tokenization.
    Example: GET /ecommerce/cart item=<NUM>
    """
    parts = [entry["method"], entry["path"]]
    for k, v in entry.get("normalized_query", {}).items():
        parts.append(f"{k}={v}")
    return " ".join(parts)

def tokenize_log(entry):
    """
    Tokenize the flattened log string and return token IDs and attention mask.
    """
    flat = flatten_log(entry)
    tokens = tokenizer(flat, return_tensors="pt")
    return {
        "input_ids": tokens["input_ids"],
        "attention_mask": tokens["attention_mask"],
        "flat_text": flat
    }

def process_logs(parsed_logs):
    """
    Tokenize a list of parsed logs and return tokenized outputs.
    """
    tokenized = []
    for entry in parsed_logs:
        result = tokenize_log(entry)
        tokenized.append(result)
    return tokenized

if __name__ == "__main__":
    # Load parsed logs from Phase 2
    with open("parsed_logs.json", "r") as f:
        parsed_logs = json.load(f)

    tokenized_output = process_logs(parsed_logs)

    # Print tokenized flat text and input IDs
    for item in tokenized_output:
        print("Text:", item["flat_text"])
        print("Token IDs:", item["input_ids"].tolist()[0])
        print("Attention Mask:", item["attention_mask"].tolist()[0])
        print("-" * 10)