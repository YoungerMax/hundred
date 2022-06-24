def max_iterable(iterable) -> float:
    a = iterable[0]

    for i in iterable:
        a = max(i, a)

    return a


def average(iterable) -> float:
    a = 0

    for i in iterable:
        a += i

    return a / len(iterable)
