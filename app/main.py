from app.observability.metrics import measure_llm_call
from app.observability.tracing import generate_request_id
from app.agents.scenic_stop_agent import ScenicStopAgent
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import google.genai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=API_KEY)

app = FastAPI(title="AI Travel LLMOps")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-llm")
def test_llm():
    def llm_call():
        return client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="Suggest one scenic stop between Pune and Goa."
        )

    response, latency, error = measure_llm_call(
        llm_call,
        agent_name="scenic_stop_agent"
    )

    if error:
        return {"error": str(error)}

    return {
        "response": response.text,
        "latency_ms": latency
    }

agent = ScenicStopAgent()

@app.get("/scenic-stop")
def scenic_stop(source: str, destination: str):
    request_id = generate_request_id()

    result = agent.suggest_stop(
        source=source,
        destination=destination,
        request_id=request_id
    )

    return {
        "request_id": request_id,
        "result": result
    }

# http://127.0.0.1:8000/scenic-stop?source=Pune&destination=Goa


