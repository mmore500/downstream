import pytest

from pylib import sign


def test_sign_positive():
    assert sign(1) == 1
    assert sign(5) == 1
    assert sign(1000) == 1
    assert sign(2**128) == 1


def test_sign_zero():
    assert sign(0) == 0


def test_sign_negative():
    assert sign(-1) == -1
    assert sign(-3) == -1
    assert sign(-999) == -1
    assert sign(-(2**128)) == -1
