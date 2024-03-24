# https://oeis.org/A005187
def get_a005187_value_at_index(n: int) -> int:
    return 2 * n - n.bit_count()
