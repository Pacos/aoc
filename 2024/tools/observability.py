import functools
import time

from loguru import logger


def monitor_exec_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()
        value = func(*args, **kwargs)
        end_time = time.perf_counter_ns()
        run_time = (end_time - start_time)/1000000
        logger.info(f"Runtime for function {func.__name__}: {run_time}ms")
        return value

    return wrapper
