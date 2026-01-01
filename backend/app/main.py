# -------------------------------------------------------------------
# Core Imports
# -------------------------------------------------------------------
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import google.genai as genai

# -------------------------------------------------------------------
# Project Imports
# -------------------------------------------------------------------
from app.observability.tracing import generate_request_id
from app.services.orchestrator import TravelOrchestrator
from app.observability.datadog_client import send_metric
from app.services.maps_service import get_route
from app.services.itinerary_service import ItineraryService

# -------------------------------------------------------------------
# Environment Setup
# -------------------------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

# -------------------------------------------------------------------
# Gemini Client
# -------------------------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

# -------------------------------------------------------------------
# FastAPI App
# -------------------------------------------------------------------
app = FastAPI(
    title="AI Travel LLMOps",
    description="Production-grade, observable multi-agent AI travel assistant",
    version="1.0.0"
)

# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# Startup Hook
# -------------------------------------------------------------------
@app.on_event("startup")
def startup_event():
    print("🚀 Backend starting — Datadog test metric")
    send_metric("backend.startup", 1)

# -------------------------------------------------------------------
# Core Services
# -------------------------------------------------------------------
orchestrator = TravelOrchestrator()
itinerary_service = ItineraryService(client)

# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------------------------------------------------
# Route API (SAFE)
# -------------------------------------------------------------------
@app.get("/route")
def route(source: str = "", destination: str = ""):
    if not source.strip() or not destination.strip():
        raise HTTPException(
            status_code=400,
            detail="Source and destination must be provided"
        )

    try:
        return get_route(source, destination)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )

# -------------------------------------------------------------------
# Trip Planning
# -------------------------------------------------------------------
@app.get("/plan-trip")
def plan_trip(source: str, destination: str, preferences: str):
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

# -------------------------------------------------------------------
# Itinerary (LLM)
# -------------------------------------------------------------------
@app.get("/itinerary")
def itinerary(
    source: str,
    destination: str,
    distance_text: str,
    duration_text: str,
):
    return itinerary_service.generate_itinerary(
        source=source,
        destination=destination,
        distance=distance_text,
        duration=duration_text,
    )
