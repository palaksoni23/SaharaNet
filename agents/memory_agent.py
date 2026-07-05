import json
import os
from datetime import datetime
from typing import List
from pydantic import BaseModel

# -------------------------
# DATA FILE
# -------------------------
DATA_FILE = "data/reports.json"


# -------------------------
# MODEL
# -------------------------
class MemoryRecord(BaseModel):
    location: str
    emergency_type: str
    priority: str
    timestamp: str
    confidence_score: float


# -------------------------
# LOAD DATA
# -------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


# -------------------------
# SAVE DATA
# -------------------------
def save_data(data):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -------------------------
# ADD NEW RECORD
# -------------------------
def add_record(report: dict):

    data = load_data()

    record = MemoryRecord(
        location=report.get("location", "unknown"),
        emergency_type=report.get("emergency_type", "unknown"),
        priority=report.get("priority", "low"),
        timestamp=str(datetime.now()),
        confidence_score=report.get("confidence_score", 0.0)
    )

    data.append(record.model_dump())

    save_data(data)

    print("\n🧠 MEMORY STORED:", record.model_dump())


# -------------------------
# ANALYZE PATTERNS
# -------------------------
def analyze_patterns():

    data = load_data()

    if not data:
        print("No memory data yet.")
        return

    location_count = {}

    for r in data:
        loc = r["location"]
        location_count[loc] = location_count.get(loc, 0) + 1

    print("\n📊 LOCATION RISK ANALYSIS:")

    for loc, count in location_count.items():
        if count >= 3:
            print(f"🚨 HIGH RISK AREA: {loc} ({count} reports)")
        elif count == 2:
            print(f"⚠️ MEDIUM RISK AREA: {loc} ({count} reports)")
        else:
            print(f"🟢 NORMAL AREA: {loc} ({count} reports)")


# -------------------------
# TEST
# -------------------------
if __name__ == "__main__":

    sample1 = {
        "location": "Alwar, Rajasthan",
        "emergency_type": "medical",
        "priority": "high",
        "confidence_score": 0.9
    }

    sample2 = {
        "location": "Alwar, Rajasthan",
        "emergency_type": "shelter",
        "priority": "critical",
        "confidence_score": 0.95
    }

    add_record(sample1)
    add_record(sample2)

    analyze_patterns()