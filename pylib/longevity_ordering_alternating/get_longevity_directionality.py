def get_longevity_directionality(longevity_level: int, polarity: bool) -> bool:
    # != gives xor
    return (polarity != bool(longevity_level % 2))
