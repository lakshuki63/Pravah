from fastapi import FastAPI
from dotenv import load_dotenv
import os
import google.genai as genai

from app.observability.tracing import generate_request_id
from app.services.orchestrator import TravelOrchestrator

# -------------------------------------------------------------------
# Environment & Client Setup
# -------------------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=API_KEY)

# -------------------------------------------------------------------
# FastAPI App
# -------------------------------------------------------------------

app = FastAPI(title="AI Travel LLMOps")

# -------------------------------------------------------------------
# Orchestrator (Single Entry Point to Agents)
# -------------------------------------------------------------------

orchestrator = TravelOrchestrator()

# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------------------------------------------------
# Trip Planning Endpoint (Orchestrated, Multi-Agent)
# -------------------------------------------------------------------

@app.get("/plan-trip")
def plan_trip(
    source: str,
    destination: str,
    preferences: str
):
    request_id = generate_request_id()

    plan = orchestrator.plan_trip(
        source=source,
        destination=destination,
        raw_preferences=preferences,
        request_id=request_id
    )

    return {
        "request_id": request_id,
        "plan": plan
    }

# Example:
# http://127.0.0.1:8000/plan-trip?source=Pune&destination=Goa&preferences=budget scenic food
