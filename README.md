# Rounding Copilot

A multi-agent AI system that helps medical teams manage patient context throughout a shift and generates structured SBAR handoff notes at shift end.

Built to solve a real problem: interns manage 10+ patients simultaneously, context gets lost between shifts, and handoff notes are written from memory under time pressure. Rounding Copilot tracks patient updates in real time and generates clinical-grade handoff notes automatically.

## Tech stack

- **Anthropic Claude** — SBAR note generation (Sonnet) and eval scoring (Opus)
- **MCP (Model Context Protocol)** — custom tool server exposing patient data to agents
- **Multi-agent orchestration** — one agent per patient, concurrent execution via asyncio
- **FastAPI + SSE** — real-time streaming of handoff notes to dashboard
- **Memory layer** — persistent shift notes stored across sessions
- **Eval harness** — LLM-as-judge scoring on completeness, accuracy, actionability

## System score

8.0/10 on automated eval suite across 10 patients (completeness, accuracy, actionability)

## How to run
```bash
# Clone and install
git clone https://github.com/Steven0x/Rounding-Copilot.git
cd Rounding-Copilot
conda create -n clinical-monitor python=3.11
conda activate clinical-monitor
pip install anthropic fastapi uvicorn httpx python-dotenv pytest "mcp[cli]"

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the API server
uvicorn main:app --reload

# Stream handoffs
curl -N http://127.0.0.1:8000/handoffs/stream

# Run evals
python evals/eval_harness.py
```

## Architecture

- `data/` — mock patient records
- `mcp_server/` — MCP tool server (get_patient, get_all_patients, add_update)
- `agents/` — safety agent (SBAR generation) and orchestrator (concurrent execution)
- `memory/` — persistent shift note store
- `evals/` — automated eval harness with LLM-as-judge
- `main.py` — FastAPI server with SSE streaming endpoint