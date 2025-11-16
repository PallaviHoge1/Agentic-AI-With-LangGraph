# tests/test_tools.py
import pytest
from src.tools.math_tools import plus, subtract, multiply, divide

def test_plus_ints():
    assert plus(5, 3) == 8

def test_subtract_float_int():
    assert abs(subtract(5.5, 2) - 3.5) < 1e-9

def test_multiply():
    assert multiply("6", "7") == 42

def test_divide_ok():
    assert divide(10, 2) == 5

def test_divide_float():
    assert abs(divide(7, 2) - 3.5) < 1e-9

def test_divide_by_zero():
    import pytest
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
