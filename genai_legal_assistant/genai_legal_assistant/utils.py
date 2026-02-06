import json
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)


def write_audit(entry: dict):
    now = datetime.utcnow().isoformat()
    fname = os.path.join(LOG_DIR, f"audit_{datetime.utcnow().date().isoformat()}.jsonl")
    entry_with_ts = {"ts": now, **entry}
    with open(fname, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry_with_ts, ensure_ascii=False) + "\n")


def read_templates(path: str):
    import json
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
