import json
from datetime import datetime

LOG_FILE = "telemetry.jsonl"
ALL_LOG_FILE = "telemetry_archive.jsonl"

def move_all_logs() -> str | None:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as src:
            data = src.read()
    except FileNotFoundError:
        return None

    if not data.strip():
        return None

    with open(ALL_LOG_FILE, "a", encoding="utf-8") as dst:
        dst.write(data)

    with open(LOG_FILE, "w", encoding="utf-8") as src:
        src.write("")

    return ALL_LOG_FILE

def clear_log():
    with open(LOG_FILE, "w") as f:
        f.write("")

def log_event(event_type, content):
    event = {
        "time": datetime.utcnow().isoformat(),
        "type": event_type,
        "content": content
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


log_event_all = log_event
