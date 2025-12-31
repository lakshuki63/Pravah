import requests
import os
import time
from app.observability.datadog_client import send_metric

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_route(source: str, destination: str):
    start_time = time.time()

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": source,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    latency_ms = (time.time() - start_time) * 1000

    if data["status"] != "OK":
        send_metric("maps.route.error", 1)
        raise Exception("Failed to fetch route")

    leg = data["routes"][0]["legs"][0]

    send_metric("maps.route.latency_ms", latency_ms)
    send_metric("maps.route.success", 1)

    return {
        "distance_text": leg["distance"]["text"],
        "duration_text": leg["duration"]["text"],
        "distance_km": leg["distance"]["value"] / 1000,
        "duration_sec": leg["duration"]["value"],
        "polyline": data["routes"][0]["overview_polyline"]["points"]
    }
