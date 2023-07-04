import pytest

import pylib


def test_positive_dividend_and_power_of_2():
    assert pylib.fast_pow2_mod(16, 1) == 0
    assert pylib.fast_pow2_mod(17, 1) == 0
    assert pylib.fast_pow2_mod(18, 1) == 0
    assert pylib.fast_pow2_mod(16, 2) == 0
    assert pylib.fast_pow2_mod(17, 2) == 1
    assert pylib.fast_pow2_mod(18, 2) == 0
    assert pylib.fast_pow2_mod(19, 2) == 1
    assert pylib.fast_pow2_mod(20, 2) == 0
    assert pylib.fast_pow2_mod(19, 4) == 3
    assert pylib.fast_pow2_mod(20, 4) == 0
    assert pylib.fast_pow2_mod(64, 1) == 0


def test_negative_dividend_and_power_of_2():
    with pytest.raises(AssertionError):
        assert pylib.fast_pow2_mod(-15, 2) == 1
    with pytest.raises(AssertionError):
        assert pylib.fast_pow2_mod(-1, 2) == 3
    with pytest.raises(AssertionError):
        assert pylib.fast_pow2_mod(-1, 3) == 7
    with pytest.raises(AssertionError):
        assert pylib.fast_pow2_mod(-16, 3) == 0


def test_zero_dividend():
    assert pylib.fast_pow2_divide(0, 4) == 0


def test_positive_dividend_and_negative_power_of_2():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(15, -2)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(1, -2)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(1, -3)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(0, -3)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(16, -3)


def test_negative_dividend_and_negative_power_of_2():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(-15, -2)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(-1, -2)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(-1, -3)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(-16, -3)


def test_zero_divisor():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(15, 0)
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(1, 0)


def test_non_power_of_2_divisor():
    with pytest.raises(AssertionError):
        pylib.fast_pow2_mod(16, 3)
