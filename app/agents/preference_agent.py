from app.observability.metrics import measure_llm_call
from app.observability.faults import maybe_fail, maybe_inject_latency


class PreferenceAgent:
    def parse_preferences(self, raw_preferences: str, request_id: str):
        """
        Preference parsing agent with fault injection.

        This agent intentionally simulates:
        - Latency spikes
        - Random failures

        Purpose:
        - Generate signal-rich telemetry
        - Test observability without burning LLM quota
        """

        def fake_llm_call():
            # Inject artificial latency (30% probability)
            maybe_inject_latency(probability=0.3)

            # Inject artificial failure (20% probability)
            maybe_fail(probability=0.2)

            # Stubbed response (no real LLM call)
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
