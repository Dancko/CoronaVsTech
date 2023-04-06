from datetime import datetime, timedelta
from typing import Callable

import pytest


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    tock = datetime.now()
    diff = tock - tick
    print(f"\nRuntime: {diff.total_seconds()}")


class PerformanceException(Exception):
    def __init__(self, runtime, runtime_limit):
        self.runtime = runtime
        self.runtime_limit = runtime_limit

    def __str__(self) -> str:
        return f"Performance test failed. Runtime: {self.runtime}, limit: {self.runtime_limit}"


def performance_tracker(func: Callable, runtime_limit=timedelta(seconds=2)):
    def run_function_and_validate_runtime(*args, **kwargs):
        tick = datetime.now()
        result = func(*args, **kwargs)
        tock = datetime.now()
        runtime = tock - tick
        print(f"\nRuntime: {runtime.total_seconds()}")

        if runtime > runtime_limit:
            raise PerformanceException(runtime=runtime, runtime_limit=runtime_limit)

        return result

    return run_function_and_validate_runtime
