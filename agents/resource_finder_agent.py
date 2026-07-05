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
class ResourceResult(BaseModel):
    hospitals: list[str]
    shelters: list[str]
    food_centers: list[str]
    immediate_actions: list[str]
    summary: str


# -------------------------
# PROMPT
# -------------------------
def build_prompt(report: dict):
    return f"""
You are SaharaNet Resource Finder Agent.

You receive a VERIFIED + SAFETY APPROVED emergency case.

Your job is to suggest REALISTIC support resources.

Focus on:
- hospitals
- shelters (NGOs, govt shelters)
- food distribution centers
- immediate survival actions

Rules:
- Be practical (India context)
- Prefer government + NGO support
- Keep suggestions realistic

INPUT:
{json.dumps(report)}

Return ONLY JSON:

{{
  "hospitals": [],
  "shelters": [],
  "food_centers": [],
  "immediate_actions": [],
  "summary": ""
}}
"""


# -------------------------
# MAIN FUNCTION
# -------------------------
def find_resources(report: dict) -> ResourceResult:

    prompt = build_prompt(report)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResourceResult
        ),
    )

    raw = response.text.strip()

    print("\n📍 RESOURCE RAW OUTPUT:\n", raw)

    return ResourceResult.model_validate_json(raw)


# -------------------------
# TEST
# -------------------------
if __name__ == "__main__":

    sample = {
        "location": "Alwar, Rajasthan",
        "emergency_type": "medical and shelter",
        "priority": "critical",
        "helpline": "108",
        "dispatch_required": True
    }

    print("\n🚀 INPUT:\n", sample)

    result = find_resources(sample)

    print("\n🔥 FINAL RESOURCE PLAN:\n")
    print(result.model_dump())