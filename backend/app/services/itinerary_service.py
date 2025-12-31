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

            # 🔎 Extract JSON safely
            match = re.search(r"\[.*\]", raw_text, re.DOTALL)
            if not match:
                raise ValueError("No JSON array found in LLM response")

            itinerary = json.loads(match.group())

            latency_ms = (time.time() - start_time) * 1000

            # -------------------------------------------------
            # ✅ SUCCESS METRICS (DASHBOARD-COMPATIBLE)
            # -------------------------------------------------

            send_metric(
                "pravah.llm.latency_ms",
                latency_ms,
                tags=["env:local", "service:pravah-backend"]
            )

            send_metric(
                "pravah.ai.itinerary.stop.count",
                len(itinerary),
                tags=["env:local", "service:pravah-backend"]
            )

            return itinerary

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000

            # -------------------------------------------------
            # ❌ FAILURE + FALLBACK METRICS (CRITICAL)
            # -------------------------------------------------

            send_metric(
                "pravah.llm.latency_ms",
                latency_ms,
                tags=["env:local", "service:pravah-backend"]
            )

            send_metric(
                "pravah.ai.fallback.used",
                1,
                tags=[
                    "env:local",
                    "reason:itinerary_generation_failed",
                    "service:pravah-backend"
                ]
            )

            return {
                "error": "Failed to generate itinerary",
                "details": str(e),
            }
