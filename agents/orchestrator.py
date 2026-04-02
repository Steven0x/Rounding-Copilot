import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from dotenv import load_dotenv
load_dotenv()

from mcp_server.tools import get_all_patients
from agents.safety_agent import generate_handoff

async def handoff_one(patient):
    patient_id = patient["patient_id"]
    name = patient["name"]
    status = patient["status"]
    print(f"Starting handoff for {name} [{status.upper()}]...")
    note = await asyncio.to_thread(generate_handoff, patient_id)
    print(f"Done: {name}")
    return {"patient_id": patient_id, "name": name, "status": status, "note": note}

async def handoff_all():
    patients = get_all_patients()
    tasks = [handoff_one(p) for p in patients]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    results = asyncio.run(handoff_all())
    print(results)
