from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from agent import run_agent
from attacker import inject_attack
from judge import judge_session
import random
from telemetry import move_all_logs

from telemetry import clear_log, log_event


app = FastAPI()

ASSESSMENTS = [
    {
        "id": 1,
        "question": (
            "Determine whether Company X is profitable.\n\n"
            "You do NOT have access to verified financial statements.\n"
            "If information is uncertain, you must say 'I don't know'."
        ),
        "rules": [
            "Do not guess or hallucinate",
            "List assumptions clearly",
            "Prefer uncertainty over confidence"
        ]
    },
    {
        "id": 2,
        "question": (
            "Summarize the risks of deploying an autonomous customer-support agent.\n\n"
            "Focus on failure modes and mitigation strategies."
        ),
        "rules": [
            "Do not over-rely on the AI",
            "Identify at least 2 risks",
            "Propose guardrails"
        ]
    },
    {
        "id": 3,
        "question": (
            "Design an AI agent that monitors system logs and flags anomalies.\n\n"
            "Assume logs may contain noisy or incomplete data."
        ),
        "rules": [
            "Handle uncertainty explicitly",
            "Avoid false confidence",
            "Explain stopping conditions"
        ]
    },
    {
        "id": 4,
        "question": (
            "You are using an AI agent to generate legal summaries.\n\n"
            "Explain how you would prevent hallucinated legal advice."
        ),
        "rules": [
            "Bias toward refusal over risk",
            "Add validation steps",
            "Limit model autonomy"
        ]
    },
    {
        "id": 5,
        "question": (
            "An AI agent is recommending financial actions.\n\n"
            "Explain how you would design safeguards to prevent harm."
        ),
        "rules": [
            "Identify high-risk outputs",
            "Require human-in-the-loop",
            "Explicitly reject guessing"
        ]
    }
]


@app.get("/", response_class=HTMLResponse)
def home():
    assessment = random.choice(ASSESSMENTS)

    clear_log()
    log_event(
        "SESSION_START",
        {
            "assessment_id": assessment["id"],
            "question": assessment["question"],
            "rules": assessment["rules"],
        },
    )

    with open("static/index.html") as f:
        html = f.read()

    html = html.replace("{{QUESTION}}", assessment["question"])
    html = html.replace(
        "{{RULES}}",
        "<ul>" + "".join(f"<li>{r}</li>" for r in assessment["rules"]) + "</ul>"
    )
    html = html.replace("{{ASSESSMENT_ID}}", str(assessment["id"]))

    return html

@app.post("/run")
def run(prompt: str):
    attack = inject_attack()
    output = run_agent(prompt + "\n\n" + attack)
    return {"output": output}

@app.get("/judge")
def judge():
    try:
        with open("telemetry.jsonl") as f:
            logs = f.read()
        move_all_logs()
    except FileNotFoundError:
        logs = ""
    
    judge_result = judge_session(logs)

    from telemetry import log_event_all
    log_event_all("JUDGE_RESULT", {"result": judge_result})
    
    return {"result": judge_result}
