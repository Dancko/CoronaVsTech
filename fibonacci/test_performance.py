import pytest
from time import sleep
from dynamic import dynamic_fib_v2
from conftest import performance_tracker


@pytest.mark.performance
@performance_tracker
def test_performance():
    dynamic_fib_v2(1000)
    sleep(3)
