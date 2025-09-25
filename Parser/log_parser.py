# This module will parse the logs into a well structured format 

import re
import json
from urllib.parse import urlparse, parse_qs


# General patter of a log for comparison purpose 
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>\d+) "[^"]*" "(?P<user_agent>[^"]+)"'
)


def normalize_value(value):
    if value.isdigit():
        return "<NUM>"
    elif re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
        return "<EMAIL>"
    elif re.match(r"^[a-f0-9\-]{36}$", value):
        return "<UUID>"
    elif re.match(r"^[A-Za-z0-9\-_]{20,}$", value):
        return "<TOKEN>"
    else:
        return "<STR>"


def normalize_query(query):
    return {k: normalize_value(v) for k, v in query.items()}


def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    data = match.groupdict()
    parsed_url = urlparse(data["url"])
    query_raw = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
    query_norm = normalize_query(query_raw)

    return {
        "ip": data["ip"],
        "timestamp": data["timestamp"],
        "method": data["method"],
        "path": parsed_url.path,
        "query": query_raw,
        "normalized_query": query_norm,
        "status": int(data["status"]),
        "user_agent": data["user_agent"]
    }

def parse_log_file(filepath):
    results = []
    with open(filepath, "r") as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                results.append(parsed)
    return results



if __name__ == "__main__":
    parsed_logs = parse_log_file("C:/xampp/apache/logs/access.log")
    count = 3
    for entry in parsed_logs:
        count -= 1
        if count > 0:
            print(json.dumps(entry, indent=2))
    
    # Save to JSON file
    with open("logs/parsed_logs.json", "w" , encoding="utf-8") as out:
        json.dump(parsed_logs, out, indent=2)

    print(f"Saved {len(parsed_logs)} parsed entries to parsed_logs.json")
