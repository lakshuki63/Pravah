from app.observability.metrics import measure_llm_call

class PreferenceAgent:
    def parse_preferences(self, raw_preferences: str, request_id: str):
        """
        NOTE:
        This is intentionally stubbed to avoid burning LLM quota.
        Later, we will replace this with a real Gemini call.
        """

        def fake_llm_call():
            return {
                "budget": "low",
                "vibe": "calm",
                "interests": ["local food"]
            }

        result, latency, error = measure_llm_call(
            fake_llm_call,
            agent_name="preference_agent",
            request_id=request_id
        )

        if error:
            raise error

        return {
            "parsed_preferences": result,
            "latency_ms": latency
        }
