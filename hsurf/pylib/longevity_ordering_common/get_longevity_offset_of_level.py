def get_longevity_offset_of_level(
    level: int,
    num_indices: int,
) -> int:
    return (num_indices >> level) & ~num_indices
