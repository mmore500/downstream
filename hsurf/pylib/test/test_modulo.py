import pytest

from pylib import modulo


def test_modulo_positive_numbers():
    assert modulo(7, 3) == 1
    assert modulo(15, 4) == 3
    assert modulo(20, 5) == 0


def test_modulo_negative_numbers():
    assert modulo(-7, 3) == 2
    assert modulo(-15, 4) == 1
    assert modulo(-20, 5) == 0


def test_modulo_mixed_signs():
    assert modulo(-7, 3) == 2
    assert modulo(7, -3) == -modulo(-7, 3)
    assert modulo(-7, -3) == -modulo(7, 3)


def test_modulo_zero():
    assert modulo(0, 3) == 0


def test_modulo_invalid_input():
    with pytest.raises(ZeroDivisionError):
        modulo(7, 0)
