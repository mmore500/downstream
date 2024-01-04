from ._get_nth_bin_width import get_nth_bin_width


def get_nth_segment_bin_width(n: int, surface_size: int) -> int:
    assert 0 <= n < surface_size.bit_count()
    assert surface_size.bit_count() == get_nth_bin_width(0, surface_size)
    return surface_size.bit_count() - n
