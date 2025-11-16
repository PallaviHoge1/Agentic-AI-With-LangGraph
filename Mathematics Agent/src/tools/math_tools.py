# src/tools/math_tools.py
from typing import Union

Number = Union[int, float]


def _to_number(x) -> Number:
    """Try to convert x to int if possible, else float.
    Raise ValueError for invalid input."""
    if isinstance(x, (int, float)):
        return x
    s = str(x).strip()
    # try int first
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            raise ValueError(f"Cannot convert '{x}' to a number.")


def plus(a, b) -> Number:
    a_n = _to_number(a)
    b_n = _to_number(b)
    res = a_n + b_n
    # if both ints, return int
    if isinstance(a_n, int) and isinstance(b_n, int):
        return int(res)
    return res


def subtract(a, b) -> Number:
    a_n = _to_number(a)
    b_n = _to_number(b)
    res = a_n - b_n
    if isinstance(a_n, int) and isinstance(b_n, int):
        return int(res)
    return res


def multiply(a, b) -> Number:
    a_n = _to_number(a)
    b_n = _to_number(b)
    res = a_n * b_n
    if isinstance(a_n, int) and isinstance(b_n, int):
        return int(res)
    return res


def divide(a, b) -> Number:
    a_n = _to_number(a)
    b_n = _to_number(b)
    if b_n == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    res = a_n / b_n
    # if division yields an integer exactly, return int
    if abs(res - round(res)) < 1e-12:
        return int(round(res))
    return res
