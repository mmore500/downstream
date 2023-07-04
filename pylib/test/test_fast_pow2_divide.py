import pytest

import pylib


def test_positive_dividend_and_divisor():
    assert pylib.fast_pow2_divide(16, 4) == 4
    assert pylib.fast_pow2_divide(17, 4) == 4
    assert pylib.fast_pow2_divide(18, 4) == 4
    assert pylib.fast_pow2_divide(19, 4) == 4
    assert pylib.fast_pow2_divide(20, 4) == 5
    assert pylib.fast_pow2_divide(32, 8) == 4
    assert pylib.fast_pow2_divide(64, 2) == 32
    assert pylib.fast_pow2_divide(16, 1) == 16  # 1 is 2^0 so this should pass
    assert pylib.fast_pow2_divide(0, 1) == 0  # 1 is 2^0 so this should pass


def test_negative_dividend_and_positive_divisor():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-15, 4)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-1, 4)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-1, 8)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-16, 8)


def test_positive_dividend_and_negative_divisor():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(15, -4)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(1, -4)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(1, -8)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(0, -8)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(16, -8)


def test_negative_dividend_and_negative_divisor():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-15, -4)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-1, -4)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-1, -8)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(-16, -8)


def test_zero_dividend():
    assert pylib.fast_pow2_divide(0, 4) == 0


def test_zero_divisor():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(15, 0)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(1, 0)


def test_non_power_of_2_divisor():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_divide(16, 3)
