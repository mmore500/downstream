def get_num_bins(surface_size: int) -> int:
    assert surface_size.bit_count() == 1  # assume even power of 2
    return surface_size >> 1  # >> 1 equivalent to // 2
