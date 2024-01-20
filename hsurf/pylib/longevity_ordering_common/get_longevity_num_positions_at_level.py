def get_longevity_num_positions_at_level(level: int) -> int:
    return 2 ** (level - 1) if level else 1
