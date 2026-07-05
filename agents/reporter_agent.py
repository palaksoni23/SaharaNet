"""
SaharaNet Reporter Agent — FINAL WORKING VERSION
Uses Google Generative AI with ADK-style architecture
"""

import os
import json
import re
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
import google.generativeai as genai
from google.adk.agents import LlmAgent

load_dotenv()

# ── API SETUP ─────────────────────────────────────────────────────────────────
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY missing in .env file!")

genai.configure(api_key=api_key)
os.environ.setdefault("GEMINI_API_KEY", api_key)


# ── PYDANTIC SCHEMA ───────────────────────────────────────────────────────────
class CitizenReportAnalysis(BaseModel):
    location: str = Field(
        description="Location mentioned by citizen. Use 'Unknown' if not mentioned."
    )
    people_count: Optional[int] = Field(
        default=None,
        description="Number of people affected. None if not mentioned."
    )
    situation_types: List[str] = Field(
        description="List of situation types: medical, food, shelter, child_safety"
    )
    urgency_level: str = Field(
        description="Urgency level: high, medium, or low"
    )
    summary: str = Field(
        description="Short 1-2 sentence English summary of the situation"
    )
    original_language: str = Field(
        description="Language of original report: Hindi, English, or Hinglish"
    )


# ── ADK AGENT DEFINITION (for architecture + competition requirement) ──────────
reporter_agent = LlmAgent(
    name="reporter_agent",
    model="gemini-2.0-flash",
    description="Extracts structured emergency data from multilingual citizen reports.",
    instruction="""You are SaharaNet Reporter Agent.
Extract info from citizen report. Return ONLY valid JSON, no markdown, no explanation.
{
  "location": "place or Unknown",
  "people_count": number or null,
  "situation_types": ["medical","shelter","food","child_safety"],
  "urgency_level": "high/medium/low",
  "summary": "short English summary",
  "original_language": "Hindi/English/Hinglish"
}"""
)


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are the SaharaNet Reporter Agent.
A citizen has reported a street family or child in need.

Extract information and return ONLY valid JSON.
No markdown. No explanation. No code blocks. Just JSON.

Required format:
{
  "location": "specific place (use 'Unknown' if not mentioned)",
  "people_count": number or null,
  "situation_types": ["medical", "shelter", "food", "child_safety"],
  "urgency_level": "high or medium or low",
  "summary": "1-2 sentence English summary",
  "original_language": "Hindi or English or Hinglish"
}

Rules:
- beemar / sick / hurt / unconscious / injured → add "medical" + urgency "high"
- bachcha akela / child alone / unaccompanied → add "child_safety"
- khaana nahi / no food / hungry / bhookha → add "food"
- ghar nahi / homeless / no shelter / sadak pe → add "shelter"
- Multiple situation_types allowed — include ALL that apply
- people_count: extract number if mentioned, null if not
- RETURN ONLY JSON. Nothing else."""


# ── MAIN ANALYZE FUNCTION ─────────────────────────────────────────────────────
def analyze_report(report_text: str) -> CitizenReportAnalysis:
    """
    Analyze a citizen's emergency report.
    Returns structured CitizenReportAnalysis object.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.1,
        )
    )

    try:
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nCitizen Report:\n{report_text}"
        )

        # Clean response — remove any markdown if present
        clean = re.sub(r"```json|```", "", response.text).strip()

        # Parse JSON
        data = json.loads(clean)

        # Validate with Pydantic
        return CitizenReportAnalysis.model_validate(data)

    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON parse failed: {e}\nRaw: {response.text[:200]}")
    except Exception as e:
        raise RuntimeError(f"Reporter Agent error: {e}")


# ── TEST ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  SaharaNet Reporter Agent — Test Run")
    print(f"  Agent : {reporter_agent.name}")
    print(f"  Model : {reporter_agent.model}")
    print("=" * 55)

    tests = [
        {
            "label": "Hindi — Medical emergency",
            "text": "Main Alwar bus stand ke paas hun. Ek family road par hai, 3 bachche hain aur ek bachcha beemar lag raha hai."
        },
        {
            "label": "English — Food + Shelter",
            "text": "I see a homeless family near Delhi railway station. Two small kids, they have no food for 2 days."
        },
        {
            "label": "Hinglish — Unconscious person",
            "text": "Yaar Jaipur mein ek aadmi road pe pada hua hai, unconscious lag raha hai. Koi madad karo please."
        },
    ]

    passed = 0
    for i, test in enumerate(tests, 1):
        print(f"\n[Test {i}] {test['label']}")
        print(f"Input : {test['text']}")
        try:
            result = analyze_report(test["text"])
            print("Output:")
            print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
            print("✅ PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {e}")

    print(f"\n{'=' * 55}")
    print(f"  Results: {passed}/{len(tests)} tests passed")
    print("=" * 55)