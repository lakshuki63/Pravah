import time
import logging

# from app.observability.datadog_client import send_test_metric
# send_test_metric()

from app.observability.datadog_client import send_metric

logger = logging.getLogger("llm_ops")
logging.basicConfig(level=logging.INFO)

def measure_llm_call(fn, agent_name: str, request_id: str):
    start = time.time()
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

        send_metric(
            "llm.agent.latency_ms",
            latency_ms,
            tags=[f"agent:{agent_name}"]
        )
        send_metric(
            "llm.agent.success",
            1,
            tags=[f"agent:{agent_name}"]
        )

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

        send_metric(
            "llm.agent.error",
            1,
            tags=[f"agent:{agent_name}"]
        )

        return None, latency_ms, e
