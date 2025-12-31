import random
import time

def maybe_inject_latency(max_delay_ms=2000, probability=0.2):
    """
    Randomly inject artificial latency.
    """
    if random.random() < probability:
        delay = random.uniform(0.5, max_delay_ms / 1000)
        time.sleep(delay)
        return delay * 1000
    return 0

def maybe_fail(probability=0.1):
    """
    Randomly raise an exception to simulate failure.
    """
    if random.random() < probability:
        raise RuntimeError("Simulated agent failure")
