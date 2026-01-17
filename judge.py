import os

from google import genai

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def judge_session(telemetry_text):
    prompt = f"""
You are a STRICT and DETERMINISTIC hiring evaluator.

Your audience is non-technical HR and hiring managers.

Rules you must follow:
You must give the same score for the same input.
Follow the scoring rubric exactly.
Be concise and direct.
Do not explain AI theory.
Do not infer intent beyond what is visible in the session log.
Do not use bullet points, symbols, markdown, or special characters.

Evaluation goal:
Assess whether this candidate can safely and responsibly work with AI systems.

Ignore:
Correctness of answers
Writing quality
Technical jargon

Only evaluate observable behavior in the session log.

Scoring rubric total score is 100.

Intent Clarity score from 0 to 25.
Clear instructions and constraints increase score.

Control and Delegation score from 0 to 25.
Candidate must control decisions.
Penalize delegation of judgment to the AI.

Safety and Guardrails score from 0 to 25.
Look for anti-hallucination rules, refusals, and limits.

Risk Awareness score from 0 to 25.
Look for detection or avoidance of unsafe outcomes.

Scoring rules:
Start each category at 0.
Add points only if clear evidence exists.
Use whole numbers only.

Session log:
{telemetry_text}

Output format exactly as follows with plain text only:

Evaluation Score: <0-100>

Intent Clarity: <0-25>
<one short sentence>

Control and Delegation: <0-25>
<one short sentence>

Safety and Guardrails: <0-25>
<one short sentence>

Risk Awareness: <0-25>
<one short sentence>

Hiring Summary:
<one short sentence stating Low risk, Medium risk, or High risk and why>
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
    )

    return response.text
