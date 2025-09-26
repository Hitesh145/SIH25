from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import json
import os

# Load and tokenize
with open("logs/labeled_dataset.json") as f:
    data = json.load(f)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
dataset = Dataset.from_list(data)
dataset = dataset.map(lambda x: tokenizer(x["text"], padding="max_length", truncation=True), batched=True)
dataset = dataset.train_test_split(test_size=0.2)

# Load model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Training config
args = TrainingArguments(
    output_dir="./model",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
)

# Train
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)

trainer.train()
trainer.save_model("./model")

predictions = trainer.predict(dataset["test"])
probs = predictions.predictions.argmax(axis=1)

with open("logs/classifier_outputs.json", "w") as f:
    json.dump([
        {"text": ex["text"], "prob_attack": float(pred[1])}
        for ex, pred in zip(dataset["test"], predictions.predictions)
    ], f, indent=2)