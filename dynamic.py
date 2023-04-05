def dynamic_fib(n: int) -> int:
    fiblist = [0, 1]

    for i in range(1, n+1):
        fiblist.append(fiblist[i] + fiblist[i - 1])

    return fiblist[n]
