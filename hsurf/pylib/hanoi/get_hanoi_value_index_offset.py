def get_hanoi_value_index_offset(value: int) -> int:
    """At what index does the hanoi value `value` first occur?"""
    return (1 << value) - 1  # 2**value - 1
