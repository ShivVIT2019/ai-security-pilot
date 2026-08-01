import streamlit as st
import requests

st.set_page_config(page_title="AI Security Pilot", page_icon="🛡️", layout="centered")

st.title("🛡️ AI Security Pilot")
st.caption("Phishing & suspicious email risk classifier — Secure AI Hackathon, Track 1")

st.markdown("Paste a suspicious email below and the system will classify its risk level, "
            "explain the evidence behind that decision, and flag it if it looks dangerous.")

email_text = st.text_area("Email content", height=200,
                           placeholder="Paste the full email text here (sender info, subject, body, links)...")

analyze_clicked = st.button("Analyze Email", type="primary")

BACKEND_URL = "http://127.0.0.1:8000/analyze"

if analyze_clicked:
    if not email_text.strip():
        st.warning("Please paste an email to analyze.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(BACKEND_URL, json={"email_text": email_text}, timeout=30)
                response.raise_for_status()
                result = response.json()

                risk_level = result.get("risk_level", "Uncertain")
                summary = result.get("summary", "No explanation returned.")
                confidence = result.get("confidence", "Low")
                flagged = result.get("flagged", False)

                # Color-code the risk level
                color_map = {"Low": "green", "Medium": "orange", "High": "red", "Uncertain": "gray"}
                color = color_map.get(risk_level, "gray")

                st.markdown(f"### Risk Level: :{color}[{risk_level}]")
                st.markdown(f"**Confidence:** {confidence}")

                if flagged:
                    st.error("🚩 This email has been flagged as potentially dangerous.")
                else:
                    st.success("✅ Not flagged as high risk.")

                st.markdown("#### Evidence & Reasoning")
                st.write(summary)

                with st.expander("Raw JSON response (for judges / debugging)"):
                    st.json(result)

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Make sure the FastAPI server is running "
                          "at http://127.0.0.1:8000 (run: uvicorn main:app --reload)")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()
st.caption("This tool provides guidance only — always verify with your organization's security team before taking action.")
