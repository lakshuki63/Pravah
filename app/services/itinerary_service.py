import time
import json
import re
import google.genai as genai
from app.observability.datadog_client import send_metric

class ItineraryService:
    def __init__(self, client: genai.Client):
        self.client = client

    def generate_itinerary(
        self,
        source: str,
        destination: str,
        distance: str,
        duration: str,
    ):
        start_time = time.time()

        prompt = f"""
You are a backend API that returns ONLY valid JSON.

Task:
Plan a road trip from {source} to {destination}.
Total distance: {distance}
Total driving time: {duration}

Return a JSON array with 3–4 stops along the route.

Each object MUST have:
- name (string)
- category (food | nature | heritage | rest)
- reason (string)
- recommended_stop_time (string)

STRICT RULES:
- Do NOT include markdown
- Do NOT include explanations
- Do NOT include backticks
- Return ONLY raw JSON
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )

            raw_text = response.text.strip()

            # 🔎 Extract JSON safely (handles extra text if any)
            match = re.search(r"\[.*\]", raw_text, re.DOTALL)
            if not match:
                raise ValueError("No JSON array found in LLM response")

            itinerary = json.loads(match.group())

            latency_ms = (time.time() - start_time) * 1000

            # ✅ Success metrics
            send_metric("llm.itinerary.latency_ms", latency_ms)
            send_metric("llm.itinerary.success", 1)
            send_metric("llm.itinerary.items_count", len(itinerary))

            return itinerary

        except Exception as e:
            # ❌ Failure metrics (VERY IMPORTANT)
            send_metric("llm.itinerary.failure", 1)

            return {
                "error": "Failed to generate itinerary",
                "details": str(e),
            }
