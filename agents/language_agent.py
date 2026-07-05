import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel

from google import genai
from google.genai import types  # Import types for configuration

load_dotenv()

# -------------------------
# CLIENT SETUP (NEW SDK)
# -------------------------
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# -------------------------
# OUTPUT SCHEMA
# -------------------------
class NormalizedReport(BaseModel):
    location: str
    people_count: int | None
    situation_types: list[str]
    urgency_score: float
    normalized_language: str
    intent: str


# -------------------------
# PROMPT
# -------------------------
def build_prompt(report: dict):
    return f"""
You are SaharaNet Language Agent.

Convert the input into a structured representation matching the requested schema.

Rules:
- location → City, State
- urgency_score:
  high = 0.9-1.0
  medium = 0.5-0.8
  low = 0.1-0.4
- normalized_language:
  Hindi → hi
  English → en
  Hinglish → en
- intent:
  emergency_assistance / information / complaint

INPUT:
{json.dumps(report)}
"""


# -------------------------
# MAIN FUNCTION
# -------------------------
def normalize_report(report: dict) -> NormalizedReport:
    prompt = build_prompt(report)

    # We pass the Pydantic model to generate_content config.
    # This forces Gemini to return a clean JSON object conforming to the schema.
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=NormalizedReport,
        ),
    )

    raw = response.text.strip()

    print("\n🔵 RAW OUTPUT:\n", raw)

    # Since response_schema guarantees valid JSON matching our model,
    # we can safely load and validate it directly.
    data = json.loads(raw)

    return NormalizedReport.model_validate(data)


# -------------------------
# TEST
# -------------------------
if __name__ == "__main__":
    sample = {
        "location": "Alwar bus stand ke paas",
        "people_count": 5,
        "situation_types": ["medical", "shelter"],
        "urgency": "high",
        "language": "Hinglish"
    }

    print("\n🚀 INPUT:\n", sample)

    result = normalize_report(sample)

    print("\n🔥 FINAL OUTPUT:\n")
    print(result.model_dump())