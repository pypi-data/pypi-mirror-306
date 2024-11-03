__import__("sys").set_int_max_str_digits(0)


def signed_max(x: int) -> int:
    return 2 ** (x - 1) - 1


def signed_min(x: int) -> int:
    return -(2 ** (x - 1))


def unsigned_max(x: int) -> int:
    return 2**x - 1


def unsigned_min():
    return 0


def float_max(x: int) -> float:
    if x == 32:
        return (2 - 2**-23) * 2**127
    elif x == 64:
        return (2 - 2**-52) * 2**1023
    else:
        raise ValueError("Unsupported bit width.")


def float_min(x: int, n: bool = True) -> float:
    if x == 32:
        return 2**-126 if n else 2**-149
    elif x == 64:
        return 2**-1022 if n else 2**-1074
    else:
        raise ValueError("Unsupported bit width.")
