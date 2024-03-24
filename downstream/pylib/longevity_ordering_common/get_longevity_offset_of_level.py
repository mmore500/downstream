def get_longevity_offset_of_level(
    level: int,
    num_indices: int,
) -> int:
    """How many physical sites from beginning does the first element of the
    nth level occur?"""
    # alternate impl: (num_indices >> level) * bool(level)
    return (num_indices >> level) & ~num_indices
