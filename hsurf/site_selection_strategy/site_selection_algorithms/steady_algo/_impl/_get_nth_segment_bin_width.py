from ._get_nth_bin_width import get_nth_bin_width
from ._get_num_segments import get_num_segments


def get_nth_segment_bin_width(n: int, surface_size: int) -> int:
    assert 0 <= n
    assert n < get_num_segments(surface_size)
    assert surface_size.bit_length() - 1 == get_nth_bin_width(0, surface_size)
    return surface_size.bit_length() - 1 - n
