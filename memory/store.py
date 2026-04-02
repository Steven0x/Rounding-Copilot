import json
import os
import threading
from datetime import datetime

MEMORY_FILE = "memory/shift_notes.json"
_lock = threading.Lock()

def save_note(patient_id: str, note: str):
    with _lock:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {}
        if patient_id not in data:
            data[patient_id] = []
        data[patient_id].append({"timestamp": datetime.now().isoformat(), "note": note})
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f)

def get_prior_notes(patient_id: str):
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)
    return data.get(patient_id, [])