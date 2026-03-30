import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import anthropic
from mcp_server.tools import get_patient, get_all_patients, add_update
from memory.store import save_note, get_prior_notes

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def generate_handoff(patient_id: str):
    patient = get_patient(patient_id)
    if "error" in patient:
        return "Patient not found"

    prior_notes = get_prior_notes(patient_id)
    prior_text = "\n".join([n['note'][:200] for n in prior_notes]) if prior_notes else "No prior notes for this patient."

    prompt = f"""
You are a clinical handoff assistant. Generate an SBAR handoff note for the following patient.

Patient: {patient['name']}, {patient['age']}yo {patient['gender']}, Room {patient['room']}
Status: {patient['status']}
Chief Complaint: {patient['chief_complaint']}
Vitals: {patient['key_vitals']}
Medical Conditions: {patient['medical_conditions']}
Procedures: {patient['medical_procedures']}

Shift Updates:
{chr(10).join(patient['updates'])}

Prior shift notes:
{prior_text}

Write a concise SBAR note with four clearly labeled sections: Situation, Background, Assessment, Recommendation.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    note = response.content[0].text
    save_note(patient_id, note)
    return note

if __name__ == "__main__":
    result = generate_handoff("P002")
    print(result)
