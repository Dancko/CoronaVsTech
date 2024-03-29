from typing import Callable

from fibonacci.naive import fibonacci
from fibonacci.cached import cached_fibs, lru_cached_fibs
from api.coronavstech.companies.dynamic import dynamic_fib, dynamic_fib_v2
import pytest


# @pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
# def test_fibs(n: int, expected: int) -> None:
#     res = fibonacci(n)
#
#     assert res == expected


@pytest.mark.parametrize("n, expected", [(40, 102334155)])
@pytest.mark.parametrize("fib_func", [fibonacci, cached_fibs, lru_cached_fibs, dynamic_fib, dynamic_fib_v2])
def test_fibs_functions(time_tracker, fib_func: Callable[[int], int], n: int, expected: int) -> None:
    res = fib_func(n)

    assert res == expected
