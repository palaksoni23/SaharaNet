import os
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# -------------------------
# OUTPUT SCHEMA
# -------------------------
class VerificationResult(BaseModel):
    is_valid: bool
    confidence_score: float  # 0 to 1
    risk_level: str          # low / medium / high / critical
    is_spam: bool
    corrected_urgency: float
    notes: str


# -------------------------
# PROMPT
# -------------------------
def build_prompt(report: dict):
    return f"""
You are SaharaNet Verification Agent.

Your job is to validate emergency reports.

INPUT:
{json.dumps(report)}

RULES:
1. Check if report is realistic
2. Detect spam / fake / joke messages
3. Assign confidence score (0 to 1)
4. Correct urgency if needed
5. Decide risk level:
   - low
   - medium
   - high
   - critical

6. Mark spam if:
   - nonsense text
   - unrealistic claims
   - missing key info

Return ONLY JSON:

{{
  "is_valid": true,
  "confidence_score": 0.0,
  "risk_level": "",
  "is_spam": false,
  "corrected_urgency": 0.0,
  "notes": ""
}}
"""


# -------------------------
# MAIN FUNCTION
# -------------------------
def verify_report(report: dict) -> VerificationResult:

    prompt = build_prompt(report)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=VerificationResult
        ),
    )

    raw = response.text.strip()

    print("\n🔵 VERIFICATION RAW OUTPUT:\n", raw)

    return VerificationResult.model_validate_json(raw)


# -------------------------
# TEST
# -------------------------
if __name__ == "__main__":

    sample = {
        "location": "Alwar, Rajasthan",
        "people_count": 5,
        "situation_types": ["medical", "shelter"],
        "urgency_score": 0.9,
        "normalized_language": "en",
        "intent": "emergency_assistance"
    }

    print("\n🚀 INPUT:\n", sample)

    result = verify_report(sample)

    print("\n🔥 FINAL VERIFICATION:\n")
    print(result.model_dump())