import pytest

import pylib


# Example functions with the enforce_types decorator
@pylib.enforce_typing
def add(a: int, b: int) -> int:
    return a + b


@pylib.enforce_typing
def concatenate(a: str, b: str) -> str:
    return a + b


def test_add_with_valid_args():
    # Test with valid argument types
    assert add(1, 2) == 3


def test_add_with_invalid_arg_type():
    # Test with invalid argument types
    with pytest.raises(TypeError):
        add(1.5, 2.5)


def test_concatenate_with_valid_args():
    # Test with valid argument types
    assert concatenate("hello", "world") == "helloworld"


def test_concatenate_with_invalid_arg_type():
    # Test with invalid argument types
    with pytest.raises(TypeError):
        concatenate("hello", 2)
