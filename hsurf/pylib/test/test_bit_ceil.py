from pylib import bit_ceil


def test_bit_ceil_at_zero():
    assert bit_ceil(0) == 1, "Expected the bit ceil of 1 to be 2"


def test_bit_ceil_at_one():
    assert bit_ceil(1) == 1, "Expected the bit ceil of 1 to be 2"


def test_bit_ceil_at_two():
    assert bit_ceil(2) == 2, "Expected the bit ceil of 2 to be 2"


def test_bit_ceil_at_three():
    assert bit_ceil(3) == 4, "Expected the bit ceil of 3 to be 4"


def test_bit_ceil_at_four():
    assert bit_ceil(4) == 4, "Expected the bit ceil of 4 to be 4"


def test_bit_ceil_at_five():
    assert bit_ceil(5) == 8, "Expected the bit ceil of 5 to be 8"


def test_bit_ceil_at_large_number():
    assert bit_ceil(1000) == 1024, "Expected the bit ceil of 1000 to be 1024"


def test_bit_ceil_at_power_of_two():
    assert bit_ceil(64) == 64, "Expected the bit ceil of 64 to be 64"


def test_bit_ceil_returns_integer():
    assert isinstance(
        bit_ceil(17), int
    ), "Expected the result to be of type int"


def test_bit_ceil_at_large_power_of_two():
    assert (
        bit_ceil(65534) == 65536
    ), "Expected the bit ceil of 65534 to be 65536"
    assert (
        bit_ceil(65536) == 65536
    ), "Expected the bit ceil of 65536 to be 65536"


def test_bit_ceil_at_one_less_than_power_of_two():
    assert bit_ceil(255) == 256, "Expected the bit ceil of 255 to be 256"
