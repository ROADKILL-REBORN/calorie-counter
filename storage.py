import json
import os

DATA_FILE = "data.json"

def _blank_day():
    return {
        "entries": [],
        "totals": {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0, "sodium": 0.0},
    }

def _load_all():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {}

def _save_all(db):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def load_day(day_key: str):
    db = _load_all()
    if day_key not in db:
        db[day_key] = _blank_day()
        _save_all(db)
    return db[day_key]

def add_entry(day_key: str, entry: dict):
    db = _load_all()
    day = db.get(day_key) or _blank_day()

    day["entries"].append(entry)

    # recompute totals
    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0, "sodium": 0.0}
    for e in day["entries"]:
        for k in totals:
            totals[k] += float(e.get(k, 0.0) or 0.0)

    day["totals"] = totals
    db[day_key] = day
    _save_all(db)

def reset_day(day_key: str):
    db = _load_all()
    db[day_key] = _blank_day()
    _save_all(db)
