import os

from google import genai

from telemetry import log_event

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a cautious research agent.
If data is uncertain, say "I don't know".
Never guess.
"""

def run_agent(user_prompt):
    log_event("USER_PROMPT", user_prompt)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "System:\n" + SYSTEM_PROMPT.strip(),
            "User:\n" + user_prompt,
        ],
    )

    output = response.text
    log_event("AGENT_OUTPUT", output)

    return output
