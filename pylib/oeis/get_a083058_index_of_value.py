from ..bit_ceil import bit_ceil


def get_a083058_index_of_value(value: int) -> int:
    assert value >= 1  # not handling 0 value
    correction = 0 < (bit_ceil(value) - value) <= value.bit_length()
    return value + value.bit_length() + (value <= 2) + correction
