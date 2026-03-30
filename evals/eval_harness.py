import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import anthropic
from agents.safety_agent import generate_handoff
from mcp_server.tools import get_all_patients

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)


def evaluate_note(patient, note):
    prompt = f"""
You are a strict clinical documentation evaluator. Score the following SBAR handoff note on three criteria.

Original patient data:
- Name: {patient['name']}, {patient['age']}yo {patient['gender']}
- Status: {patient['status']}
- Chief complaint: {patient['chief_complaint']}
- Vitals: {patient['key_vitals']}
- Updates: {', '.join(patient['updates'])}

Generated SBAR note:
{note}

Score each criterion from 1-10:
1. Completeness: Does the note include all key patient information?
2. Accuracy: Does the note correctly reflect the patient data?
3. Actionability: Are the recommendations specific and useful?

Respond in this exact JSON format:
{{
    "completeness": <score>,
    "accuracy": <score>,
    "actionability": <score>,
    "reasoning": "<one sentence explanation>"
}}
"""
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.content[0].text)


def run_evals():
    patients = get_all_patients()
    results = []

    for patient in patients:
        print(f"Evaluating {patient['name']}...")
        note = generate_handoff(patient["patient_id"])
        scores = evaluate_note(patient, note)
        avg = round((scores["completeness"] + scores["accuracy"] + scores["actionability"]) / 3, 1)
        results.append({
            "patient": patient["name"],
            "status": patient["status"],
            "scores": scores,
            "average": avg
        })
        print(f"  {patient['name']}: {avg}/10 — {scores['reasoning']}")

    overall = round(sum(r["average"] for r in results) / len(results), 1)
    print(f"\nOverall system score: {overall}/10")
    return results


if __name__ == "__main__":
    run_evals()

    