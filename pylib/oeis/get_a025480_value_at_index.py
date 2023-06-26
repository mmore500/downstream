def get_a025480_value_at_index(n: int) -> int:
    # https://oeis.org/A025480
    return n >> ((~(n + 1) & n).bit_length() + 1)
