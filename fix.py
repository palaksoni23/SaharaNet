content = open('app.py', encoding='utf-8').read()

old = '''def analyze(text: str) -> dict:
    """Call Gemini directly — no ADK overhead in UI layer."""
    from google import genai
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    PROMPT = """Extract from citizen report. Return ONLY valid JSON, no markdown:
{
  "location": "place name or Unknown",
  "people_count": null,
  "situation_types": ["medical","shelter","food","child_safety"],
  "urgency_level": "high or medium or low",
  "summary": "short English summary",
  "original_language": "Hindi or English or Hinglish"
}
Rules: beemar/sick=medical+high, bachcha/child=child_safety, khaana nahi=food, ghar nahi=shelter"""

    model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.1
    )
)
    res = model.generate_content(f"{PROMPT}\\n\\nReport: {text}")
    clean = re.sub(r"```json|```", "", res.text).strip()
    return json.loads(clean)'''

new = '''def analyze(text: str) -> dict:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    PROMPT = """Extract from citizen report. Return ONLY valid JSON, no markdown:
{
  "location": "place name or Unknown",
  "people_count": null,
  "situation_types": ["medical","shelter","food","child_safety"],
  "urgency_level": "high or medium or low",
  "summary": "short English summary",
  "original_language": "Hindi or English or Hinglish"
}
Rules: beemar/sick=medical+high, bachcha/child=child_safety, khaana nahi=food, ghar nahi=shelter"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        ),
        contents=f"{PROMPT}\\n\\nReport: {text}"
    )
    clean = re.sub(r"```json|```", "", response.text).strip()
    return json.loads(clean)'''

result = content.replace(old, new)
if result == content:
    print("ERROR: Match nahi hua!")
else:
    open('app.py', 'w', encoding='utf-8').write(result)
    print("Done! app.py updated successfully!")