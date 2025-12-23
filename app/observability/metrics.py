import time
import logging

logger = logging.getLogger("llm_ops")
logging.basicConfig(level=logging.INFO)

def measure_llm_call(fn, agent_name: str, request_id: str):
    start = time.time()
    try:
        result = fn()
        duration = (time.time() - start) * 1000  # ms

        logger.info(
            f"request_id={request_id} "
            f"agent={agent_name} "
            f"status=success "
            f"latency_ms={duration:.2f}"
        )

        return result, duration, None

    except Exception as e:
        duration = (time.time() - start) * 1000

        logger.error(
            f"request_id={request_id} "
            f"agent={agent_name} "
            f"status=error "
            f"latency_ms={duration:.2f} "
            f"error={str(e)}"
        )

        return None, duration, e
