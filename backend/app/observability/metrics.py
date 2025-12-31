# app/observability/metrics.py

import time
import logging
from app.observability.datadog_client import send_metric

logger = logging.getLogger("llm_ops")
logging.basicConfig(level=logging.INFO)

SERVICE_TAGS = [
    "service:pravah-backend",
    "version:v1"
]

def measure_llm_call(
    fn,
    agent_name: str,
    request_id: str,
    model="gemini-2.5-flash",
    env="local"
):
    start = time.time()

    tags = [
        f"agent:{agent_name}",
        f"model:{model}",
        f"env:{env}",
        *SERVICE_TAGS
    ]

    try:
        result = fn()
        latency_ms = (time.time() - start) * 1000

        logger.info(
            "llm.agent.success",
            extra={
                "agent": agent_name,
                "request_id": request_id,
                "latency_ms": latency_ms
            }
        )

        # 🔢 Core metrics
        send_metric("pravah.llm.request.count", 1, tags, metric_type="count")
        send_metric("pravah.llm.latency_ms", latency_ms, tags, metric_type="distribution")
        send_metric("pravah.llm.response.success", 1, tags, metric_type="count")

        return result, latency_ms, None

    except Exception as e:
        latency_ms = (time.time() - start) * 1000

        logger.error(
            "llm.agent.error",
            extra={
                "agent": agent_name,
                "request_id": request_id,
                "latency_ms": latency_ms,
                "error": str(e)
            }
        )

        send_metric("pravah.llm.request.count", 1, tags, metric_type="count")
        send_metric("pravah.llm.latency_ms", latency_ms, tags, metric_type="distribution")
        send_metric("pravah.llm.response.failure", 1, tags, metric_type="count")

        return None, latency_ms, e
