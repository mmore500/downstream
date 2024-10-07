def bit_floor(x: int) -> int:
    """Return the largest power of two less than or equal to x."""
    assert x > 0
    return 1 << (x.bit_length() - 1)