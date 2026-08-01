import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI(title="AI Security Pilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    email_text: str


PROMPT_TEMPLATE = """You are a security analyst reviewing an email for phishing risk.

Analyze the following email and respond with ONLY a JSON object (no markdown, no code fences, no extra text) in exactly this format:

{{
  "risk_level": "Low" | "Medium" | "High" | "Uncertain",
  "summary": "one or two sentence explanation of your reasoning",
  "confidence": "High" | "Low",
  "flagged": true | false
}}

Rules:
- Use "Uncertain" for risk_level if the email does not contain enough information to make a confident judgment.
- Base your judgment on concrete signals: sender/domain mismatch, urgency or threat language, suspicious links, requests for credentials or payment, spoofed branding, grammar/formatting anomalies.
- confidence should be "Low" if the email is short, ambiguous, or lacks clear signals either way.
- flagged should be true only if risk_level is "Medium" or "High".
- Do not invent details that are not present in the email text.

Email to analyze:
---
{email_text}
---
"""


@app.post("/analyze")
def analyze_email(request: EmailRequest):
    prompt = PROMPT_TEMPLATE.format(email_text=request.email_text)

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        result = json.loads(raw_text)

        result.setdefault("risk_level", "Uncertain")
        result.setdefault("summary", "Model did not return a clear explanation.")
        result.setdefault("confidence", "Low")
        result.setdefault("flagged", False)

        return result

    except (json.JSONDecodeError, Exception) as e:
        return {
            "risk_level": "Uncertain",
            "summary": f"Could not confidently analyze this email. Error: {str(e)}",
            "confidence": "Low",
            "flagged": False,
        }


@app.get("/")
def health_check():
    return {"status": "ok", "service": "AI Security Pilot backend"}
