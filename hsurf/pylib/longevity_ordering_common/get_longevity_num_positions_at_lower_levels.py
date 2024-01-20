def get_longevity_num_positions_at_lower_levels(longevity_level: int) -> int:
    # level -> num_positions_at_lower_levels
    # 0 -> 0
    # 1 -> 1
    # 2 -> 2, etc.
    # 3 -> 4, etc.
    return 2 ** (longevity_level - 1) if longevity_level else 0
