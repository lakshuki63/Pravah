from app.agents.scenic_stop_agent import ScenicStopAgent
from app.agents.preference_agent import PreferenceAgent

class TravelOrchestrator:
    def __init__(self):
        self.scenic_agent = ScenicStopAgent()
        self.preference_agent = PreferenceAgent()

    def plan_trip(self, source, destination, raw_preferences, request_id):
        preferences = self.preference_agent.parse_preferences(
            raw_preferences=raw_preferences,
            request_id=request_id
        )

        scenic_stop = self.scenic_agent.suggest_stop(
            source=source,
            destination=destination,
            request_id=request_id
        )

        return {
            "preferences": preferences,
            "scenic_stop": scenic_stop
        }
