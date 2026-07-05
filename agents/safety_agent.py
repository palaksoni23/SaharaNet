import os
import json
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# -------------------------
# OUTPUT SCHEMA
# -------------------------
class SafetyDecision(BaseModel):
    emergency_type: str          # medical / police / child / shelter / unknown
    priority: str                # critical / high / medium / low
    helpline: str                # 108 / 100 / 1098 / NGO / none
    action_plan: list[str]       # step-by-step actions
    dispatch_required: bool
    notes: str


# -------------------------
# PROMPT
# -------------------------
def build_prompt(report: dict):
    return f"""
You are SaharaNet Safety Agent.

You receive a VERIFIED emergency report.

Your job:
- classify emergency type
- assign priority
- choose correct helpline
- create action plan
- decide dispatch requirement

IMPORTANT HELPLINES:
- medical emergency → 108
- police → 100
- child safety → 1098
- shelter / homeless → NGO support

INPUT:
{json.dumps(report)}

Return ONLY JSON:

{{
  "emergency_type": "",
  "priority": "",
  "helpline": "",
  "action_plan": [],
  "dispatch_required": true,
  "notes": ""
}}
"""


# -------------------------
# MAIN FUNCTION
# -------------------------
def analyze_safety(report: dict) -> SafetyDecision:

    prompt = build_prompt(report)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SafetyDecision
        ),
    )

    raw = response.text.strip()

    print("\n🚨 SAFETY RAW OUTPUT:\n", raw)

    return SafetyDecision.model_validate_json(raw)


# -------------------------
# TEST
# -------------------------
if __name__ == "__main__":

    sample = {
        "location": "Alwar, Rajasthan",
        "people_count": 5,
        "situation_types": ["medical", "shelter"],
        "urgency_score": 0.9,
        "confidence_score": 0.92,
        "intent": "emergency_assistance"
    }

    print("\n🚀 INPUT:\n", sample)

    result = analyze_safety(sample)

    print("\n🔥 FINAL SAFETY DECISION:\n")
    print(result.model_dump())