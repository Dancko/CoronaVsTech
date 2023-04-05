from functools import lru_cache


cache = {}


def cached_fibs(n: int) -> int:
    if n in cache:
        return cache[n]

    if n == 0 or n == 1:
        return n
    else:
        fn = cached_fibs(n - 1) + cached_fibs(n - 2)
        cache[n] = fn
        return fn


@lru_cache(maxsize=256)
def lru_cached_fibs(n: int) -> int:
    if n == 0 or n == 1:
        return n
    return lru_cached_fibs(n - 1) + lru_cached_fibs(n - 2)
