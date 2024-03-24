def get_hanoi_value_index_cadence(value: int) -> int:
    """How many indices occur between instances of hanoi value `value` after its
    first occurrence?"""
    return 1 << (value + 1)  # 2 ** (value + 1)
