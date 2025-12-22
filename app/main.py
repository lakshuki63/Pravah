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
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",  # <--- Changed from gemini-1.5-pro
            contents="Suggest one scenic stop between Pune and Goa."
        )
        return {"response": response.text}
    except Exception as e:
        # This will help you see the error in the browser/Postman instead of just a 500
        return {"error": str(e)}
