import os

from openai import OpenAI

from telemetry import log_event

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """
You are a cautious research agent.
If data is uncertain, say "I don't know".
Never guess.
"""

def run_agent(user_prompt):
    log_event("USER_PROMPT", user_prompt)

    response = client.chat.completions.create(
        model="z-ai/glm-4.5-air:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": user_prompt},
        ],
    )

    output = response.choices[0].message.content
    log_event("AGENT_OUTPUT", output)

    return output
