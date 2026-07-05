"""
SaharaNet Reporter Agent Module (DEBUG VERSION)
"""

import os
import json
import asyncio
from typing import List, Optional, Union, Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner

load_dotenv()

# API KEY FIX
google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key:
    os.environ["GEMINI_API_KEY"] = google_api_key


# -------------------------
# STRUCTURED OUTPUT SCHEMA
# -------------------------
class CitizenReportAnalysis(BaseModel):
    location: str = Field(description="Location of the incident. Use 'Unknown' if missing.")
    people_count: Optional[int] = Field(default=None, description="Number of affected people if mentioned.")
    situation_types: List[str] = Field(description="medical, food, shelter, child safety")
    urgency_level: str = Field(description="high, medium or low")
    summary: str = Field(description="Short English summary of the incident.")
    original_language: str = Field(description="Hindi, English or Hinglish")


# -------------------------
# AGENT
# -------------------------
reporter_agent = LlmAgent(
    name="reporter_agent",
    model="gemini-2.5-flash",
    description="Extracts structured emergency data from citizen reports.",
    instruction="""You are SaharaNet Reporter Agent.

RESPOND ONLY WITH VALID JSON. NO OTHER TEXT. NO MARKDOWN.

{
  "location": "string",
  "people_count": null or number,
  "situation_types": ["medical", "food", "shelter", "child safety"],
  "urgency_level": "high or medium or low",
  "summary": "short summary in English",
  "original_language": "Hindi or English or Hinglish"
}""",
)


# -------------------------
# PUBLIC FUNCTION
# -------------------------
def analyze_report(report_text: str) -> CitizenReportAnalysis:
    """Synchronous wrapper for analyzing a citizen report."""
    return asyncio.run(_analyze_report(report_text))


# -------------------------
# CORE LOGIC (DEBUG)
# -------------------------
async def _analyze_report(report_text: str) -> CitizenReportAnalysis:
    """
    Analyzes a citizen report and returns structured data.
    With debug output.
    """

    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GOOGLE_API_KEY is missing in .env")

    runner = InMemoryRunner(agent=reporter_agent)

    try:
        result = await runner.run(user_messages=report_text)

        # 🔍 DEBUG: Print structure
        print(f"\n[DEBUG] Result type: {type(result)}")
        print(f"[DEBUG] Result dir: {[attr for attr in dir(result) if not attr.startswith('_')]}")
        print(f"[DEBUG] Result str: {str(result)[:500]}")

        # Try to get response
        response_text = None

        # Pattern 1: .text (most common for LLM responses)
        if hasattr(result, "text"):
            response_text = result.text
            print(f"[DEBUG] Found .text: {response_text[:200]}")

        # Pattern 2: .content
        elif hasattr(result, "content"):
            response_text = result.content
            print(f"[DEBUG] Found .content: {response_text[:200]}")

        # Pattern 3: .output
        elif hasattr(result, "output"):
            response_text = result.output
            print(f"[DEBUG] Found .output: {response_text[:200]}")

        # Pattern 4: Last message
        elif hasattr(result, "messages") and result.messages:
            last_msg = result.messages[-1]
            print(f"[DEBUG] Last message type: {type(last_msg)}")
            if hasattr(last_msg, "content"):
                response_text = last_msg.content
            elif hasattr(last_msg, "text"):
                response_text = last_msg.text
            print(f"[DEBUG] Found in messages: {str(response_text)[:200]}")

        if not response_text:
            print(f"[DEBUG] No response found in any pattern!")
            print(f"[DEBUG] Full result: {vars(result) if hasattr(result, '__dict__') else result}")
            raise RuntimeError("No response from agent")

        # Parse JSON
        response_text = str(response_text).strip()
        
        # Remove markdown if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()

        print(f"[DEBUG] Cleaned response: {response_text[:300]}")

        # Parse as JSON
        parsed = json.loads(response_text)
        return CitizenReportAnalysis.model_validate(parsed)

    except json.JSONDecodeError as je:
        print(f"[DEBUG] JSON parse error: {je}")
        raise RuntimeError(f"Reporter Agent failed: Invalid JSON - {je}")
    except Exception as error:
        print(f"[DEBUG] Exception: {type(error).__name__}: {error}")
        raise RuntimeError(f"Reporter Agent failed: {error}")
    finally:
        await runner.close()


if __name__ == "__main__":
    print("SaharaNet Reporter Agent loaded successfully")