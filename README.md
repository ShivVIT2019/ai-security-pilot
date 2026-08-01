# AI Security Pilot

**Secure AI Hackathon — Track 1: Security Reasoning Agent**
Seattle Data AI & Security Community

Video Link - https://youtu.be/vnnTWP0wkrs


Built by:

[Atchyut](https://github.com/ShivVIT2019) and [Shreya](https://github.com/ssb1506)

## Problem

Non-technical users receive phishing and suspicious emails regularly and often can't
tell whether a message is dangerous. AI Security Pilot lets a user paste an email and
get back a clear, evidence-backed risk assessment instead of a blind AI guess.

## What it does

1. **Input** — user pastes raw email text (sender info, subject, body, links) into the UI.
2. **AI analysis** — the backend sends the email to Gemini with a structured prompt and
   classifies risk as `Low`, `Medium`, `High`, or `Uncertain`.
3. **Evidence** — the response includes a short explanation citing concrete signals
   (urgency language, sender/domain mismatch, suspicious links, credential requests).
4. **Trust / safety layer** — if the email doesn't contain enough signal to make a
   confident call, the system returns `"Uncertain"` with `"confidence": "Low"` instead
   of forcing a verdict. This is tested and demonstrated in the demo video.

## Architecture

```
User (Streamlit UI)
      |
      v
POST /analyze  (FastAPI backend)
      |
      v
Gemini (gemini-2.5-flash) — structured JSON risk classification
      |
      v
Response: { risk_level, summary, confidence, flagged }
```

## Tech stack

- **Backend:** FastAPI (Python)
- **AI:** Google Gemini (`google-generativeai`), model `gemini-2.5-flash`
- **Frontend:** Streamlit
- **Environment management:** python-dotenv

## Setup & running locally

1. Clone the repo and enter the project folder:
   ```
   git clone https://github.com/ShivVIT2019/ai-security-pilot.git
   cd ai-security-pilot
   ```

2. Create a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn google-generativeai python-dotenv streamlit requests
   ```

3. Get a Gemini API key from https://aistudio.google.com/apikey and create a `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```

4. Start the backend (in one terminal):
   ```
   uvicorn main:app --reload
   ```
   The API will be live at `http://127.0.0.1:8000` (interactive docs at `/docs`).

5. Start the frontend (in a second terminal, same venv):
   ```
   streamlit run app.py
   ```

6. Paste a suspicious email into the UI and click **Analyze Email**.

## API contract

**POST** `/analyze`

Request:
```json
{ "email_text": "..." }
```

Response:
```json
{
  "risk_level": "Low | Medium | High | Uncertain",
  "summary": "short explanation of the reasoning",
  "confidence": "High | Low",
  "flagged": true
}
```

## Dataset / API disclosure

- No pre-existing or private dataset used. Sample emails used for testing/demo are
  synthetic examples written for this project.
- AI component: Google Gemini API (`gemini-2.5-flash`), used as a disclosed third-party
  dependency for risk classification and explanation generation.
- No confidential, private, or unlawfully obtained data is used anywhere in this project.

## Known limitations

- Risk classification depends on the language model's judgment; it is not a substitute
  for organizational security review.
- Evidence extraction currently comes from the LLM's own reasoning rather than an
  independent rules/regex layer — a good next step for future iteration.
- No persistent storage/audit log in this version; each request is stateless.

## Team 

**Binghamton University**
- **Atchyut** ([ShivVIT2019](https://github.com/ShivVIT2019)) — FastAPI backend, Gemini integration, prompt design
- **Shreya** ([ssb1506](https://github.com/ssb1506)) — Frontend, testing, demo,Presentation Preparation
