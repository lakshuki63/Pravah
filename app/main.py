from fastapi import FastAPI
from dotenv import load_dotenv
import os
from google import genai

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
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Suggest one scenic stop between Pune and Goa."
    )
    return {"response": response.text}
