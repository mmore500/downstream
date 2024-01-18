def get_a037870_value_at_index(n: int) -> int:
    # https://oeis.org/A037870
    assert n.bit_count()
    mask = (1 << n.bit_count()) - 1
    return n.bit_count() - (n & mask).bit_count()
