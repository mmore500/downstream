def get_longevity_offset_of_level(
    level: int,
    num_indices: int,
) -> int:
    return num_indices // 2**level if level else 0
