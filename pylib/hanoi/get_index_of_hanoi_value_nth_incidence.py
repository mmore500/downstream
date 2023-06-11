def get_index_of_hanoi_value_nth_incidence(value: int, i: int) -> int:
    offset = 2 ** value - 1
    cadence = 2 ** (value + 1)
    return offset + cadence * i
