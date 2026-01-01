import requests
import os
import time
from app.observability.datadog_client import send_metric

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_route(source: str, destination: str):
    if not source or not destination:
        raise ValueError("Source or destination missing")

    start = time.time()

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": source,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY
    }

    res = requests.get(url, params=params)
    data = res.json()

    latency_ms = (time.time() - start) * 1000

    if data.get("status") != "OK":
        send_metric("maps.route.error", 1)
        raise Exception(data.get("error_message", "Route failed"))

    leg = data["routes"][0]["legs"][0]

    send_metric("maps.route.latency_ms", latency_ms)
    send_metric("maps.route.success", 1)

    return {
        "distance_text": leg["distance"]["text"],
        "duration_text": leg["duration"]["text"],
        "distance_km": leg["distance"]["value"] / 1000,
        "duration_sec": leg["duration"]["value"],
        "polyline": data["routes"][0]["overview_polyline"]["points"],
    }
