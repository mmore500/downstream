def get_longevity_level_of_index(index: int) -> int:
    """What physical nesting layer does the logical index map to?"""
    return index.bit_length()
