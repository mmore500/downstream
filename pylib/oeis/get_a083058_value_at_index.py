def get_a083058_value_at_index(n: int) -> int:
    return n - n.bit_length() + (n == 1)
