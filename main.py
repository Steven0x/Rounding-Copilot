import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json
from agents.orchestrator import handoff_one
from mcp_server.tools import get_all_patients


app= FastAPI()
async def stream_handoffs():
    patients = get_all_patients()
    tasks = [handoff_one(p) for p in patients]
    
    for coro in asyncio.as_completed(tasks):
        result = await coro
        data = json.dumps(result)
        yield f"data: {data}\n\n"

@app.get("/handoffs/stream")
async def handoffs_stream():
    return StreamingResponse(
        stream_handoffs(),
        media_type="text/event-stream"
    )

    