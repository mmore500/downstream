from .....pylib import bit_floor
from ._get_nth_segment_bin_width import get_nth_segment_bin_width
from ._get_nth_segment_position import get_nth_segment_position
from ._get_num_bins import get_num_bins


def get_nth_bin_position(n: int, surface_size: int) -> int:
    # with bin positions distributed per get_nth_bin_width, how many positions
    # over does the nth bin start?
    # this is the sum of the widths of all bins before the nth bin
    assert 0 <= n < get_num_bins(surface_size)
    assert surface_size.bit_count() == 1  # assume perfect power of 2

    if n == 0:  # special-case the zeroth segment
        return 0
    n -= 1  # we've handled one bin

    # get the next all-1s number less than or equal to n
    # subtract one from perfect square gets an all 1's number
    completed_bins = bit_floor(n + 1) - 1
    assert completed_bins.bit_length() == completed_bins.bit_count()
    assert n // 2 <= completed_bins <= n
    completed_segments = 1 + completed_bins.bit_length()  # include 0th segment

    position = get_nth_segment_position(completed_segments, surface_size)

    # ... and now handle the remaining partially-filled bin segment, if any
    num_unhandled_bins = n - completed_bins
    if num_unhandled_bins:
        unhandled_segment_bin_width = get_nth_segment_bin_width(
            completed_segments, surface_size
        )
        position += num_unhandled_bins * unhandled_segment_bin_width

    return position
