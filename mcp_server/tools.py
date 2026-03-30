import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from data.mock_patients import patients

mcp = FastMCP("rounding-copilot")




@mcp.tool()
def get_patient(patient_id: str):
    for p in patients:
        if p["patient_id"] == patient_id:
            return p
    return {"error": "Patient not found"}


@mcp.tool()
def get_all_patients():
    return patients



@mcp.tool()
def add_update(patient_id: str, update: str):
    for p in patients:
        if p["patient_id"] == patient_id:
            p["updates"].append(update)
            return {"success": True, "patient_id": patient_id}
    return {"error": "Patient not found"}

if __name__ == "__main__":
    mcp.run()