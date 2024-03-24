from ._get_nth_segment_bin_count import get_nth_segment_bin_count
from ._get_nth_segment_bin_width import get_nth_segment_bin_width


def get_nth_segment_width(n: int, surface_size: int) -> int:
    return get_nth_segment_bin_count(n) * get_nth_segment_bin_width(
        n, surface_size
    )
