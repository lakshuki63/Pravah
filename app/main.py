# -------------------------------------------------------------------
# Core Imports
# -------------------------------------------------------------------

from fastapi import FastAPI
from dotenv import load_dotenv
import os

# -------------------------------------------------------------------
# Project Imports
# -------------------------------------------------------------------

from app.observability.tracing import generate_request_id
from app.services.orchestrator import TravelOrchestrator
from app.observability.datadog_client import send_metric

# -------------------------------------------------------------------
# Environment Setup
# -------------------------------------------------------------------

load_dotenv()

# Validate Gemini API key early
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

# -------------------------------------------------------------------
# FastAPI App
# -------------------------------------------------------------------

app = FastAPI(
    title="AI Travel LLMOps",
    description="Production-grade, observable multi-agent AI travel assistant",
    version="1.0.0"
)

# -------------------------------------------------------------------
# Startup Hook (Datadog Integration Test)
# -------------------------------------------------------------------

@app.on_event("startup")
def startup_event():
    print("🚀 Application starting — sending Datadog test metric...")
    send_metric(
        metric_name="llm.integration.test",
        value=1,
        tags=["env:local", "component:startup"]
    )

# -------------------------------------------------------------------
# Orchestrator
# -------------------------------------------------------------------

orchestrator = TravelOrchestrator()

# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------------------------------------------------
# Trip Planning Endpoint
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

from app.services.maps_service import get_route

@app.get("/route")
def route(source: str, destination: str):
    return get_route(source, destination)

# Example:
# http://127.0.0.1:8000/plan-trip?source=Pune&destination=Goa&preferences=budget calm scenic food
