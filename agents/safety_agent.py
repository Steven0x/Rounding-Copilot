import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

import anthropic
from mcp_server.tools import get_patient, get_all_patients, add_update
client = anthropic.Anthropic(api_key=api_key)

def generate_handoff(patient_id: str):
    patient = get_patient(patient_id)
    if "error" in patient:
        return "Patient not found"
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

Write a concise SBAR note with four clearly labeled sections: Situation, Background, Assessment, Recommendation.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text


if __name__ == "__main__":
    result = generate_handoff("P002")
    print(result)
