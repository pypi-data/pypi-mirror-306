from sys import set_int_max_str_digits

set_int_max_str_digits(0) # To remove the limit for integer string conversion.


def signed_max(x: int) -> int:
    """
    Calculate the maximum value for a signed integer of given bit width.

    Args:
        x (int): The bit width of the signed integer.

    Returns:
        int: The maximum value for the signed integer.
    """
    return 2 ** (x - 1) - 1


def signed_min(x: int) -> int:
    """
    Calculate the minimum value for a signed integer of given bit width.

    Args:
        x (int): The bit width of the signed integer.

    Returns:
        int: The minimum value for the signed integer.
    """
    return -(2 ** (x - 1))


def unsigned_max(x: int) -> int:
    """
    Calculate the maximum value for an unsigned integer of given bit width.

    Args:
        x (int): The bit width of the unsigned integer.

    Returns:
        int: The maximum value for the unsigned integer.
    """
    return 2**x - 1


def unsigned_min(x: int = 0) -> int:
    """
    Calculate the minimum value for an unsigned integer.

    Args:
        x (int, optional): The bit width of the unsigned integer (default is 0).

    Returns:
        int: The minimum value for the unsigned integer (always 0).
    """
    return 0


def float_max(x: int) -> float:
    """
    Calculate the maximum value for a floating-point number of given bit width.

    Args:
        x (int): The bit width of the floating-point number (32 or 64).

    Returns:
        float: The maximum value for the floating-point number, or None if unsupported.
    """
    if x == 32:
        return (2 - 2**-23) * 2**127
    elif x == 64:
        return (2 - 2**-52) * 2**1023
    else:
        return None


def float_min(x: int, n: bool = True) -> float:
    """
    Calculate the minimum positive normalized or denormalized value for a floating-point number of given bit width.

    Args:
        x (int): The bit width of the floating-point number (32 or 64).
        n (bool, optional): If True, returns the minimum normalized value; if False, returns the minimum denormalized value (default is True).

    Returns:
        float: The minimum value for the floating-point number, or None if unsupported.
    """
    if x == 32:
        if n:
            return 2**-126
        else:
            return 2**-149
    elif x == 64:
        if n:
            return 2**-1022
        else:
            return 2**-1074
    else:
        return None
