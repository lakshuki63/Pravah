# -------------------------------------------------------------------
# Datadog API-based Metrics Client (No Agent Required)
# -------------------------------------------------------------------

import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Datadog configuration
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")

# IMPORTANT: use the exact site shown in your Datadog UI
DATADOG_SITE = "us5.datadoghq.com"

# Datadog Metrics API endpoint
BASE_URL = f"https://api.{DATADOG_SITE}/api/v1/series"

if not DATADOG_API_KEY:
    raise RuntimeError("DATADOG_API_KEY not found in environment")

def send_metric(metric_name: str, value: float, tags=None):
    """
    Send a single custom metric to Datadog via HTTPS.
    This works without the Datadog Agent and is ideal for
    local development, hackathons, and Cloud Run.
    """

    payload = {
        "series": [
            {
                "metric": metric_name,
                "points": [[int(time.time()), value]],
                "type": "gauge",
                "tags": tags or []
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DATADOG_API_KEY
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)

    # Critical debug output — DO NOT remove until verified
    print("Datadog response:", response.status_code, response.text)
