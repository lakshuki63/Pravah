import os
import google.genai as genai
from dotenv import load_dotenv
from app.observability.metrics import measure_llm_call

load_dotenv()

class ScenicStopAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash-lite"

    def suggest_stop(self, source: str, destination: str, request_id: str):
        prompt = (
            f"Suggest one scenic stop between {source} and {destination}. "
            "Provide a brief reason why it is worth visiting."
        )

        def llm_call():
            return self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

        response, latency, error = measure_llm_call(
    llm_call,
    agent_name="scenic_stop_agent",
    request_id=request_id
)


        if error:
            raise error

        return {
            "text": response.text,
            "latency_ms": latency
        }
