def dynamic_fib(n: int) -> int:
    fiblist = [0, 1]

    for i in range(1, n+1):
        fiblist.append(fiblist[i] + fiblist[i - 1])

    return fiblist[n]


def dynamic_fib_v2(n: int) -> int:
    fib1, fib2 = 0, 1

    for i in range(1, n + 1):
        fi = fib1 + fib2
        fib1, fib2 = fib2, fi

    return fib1


print(dynamic_fib_v2(6))
