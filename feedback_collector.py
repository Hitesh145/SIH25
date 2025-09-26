import json
import os

os.makedirs("logs", exist_ok=True)

def collect_feedback(text, model_score, label, analyst_decision):
    entry = {
        "text": text,
        "model_score": model_score,
        "model_label": label,
        "analyst_decision": analyst_decision
    }

    try:
        with open("logs/feedback_log.json", "r") as f:
            feedback = json.load(f)
    except FileNotFoundError:
        feedback = []

    feedback.append(entry)

    with open("logs/feedback_log.json", "w") as f:
        json.dump(feedback, f, indent=2)

    print("Feedback saved.")

# Example usage
collect_feedback(
    text="GET /admin?user=admin' OR '1'='1",
    model_score=0.87,
    label="suspicious",
    analyst_decision="benign"
)