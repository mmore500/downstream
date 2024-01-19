def get_hanoi_value_index_offset(value: int) -> int:
    return (1 << value) - 1  # 2**value - 1
