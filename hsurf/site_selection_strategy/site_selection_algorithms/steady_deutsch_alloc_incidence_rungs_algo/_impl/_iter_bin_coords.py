import itertools as it
import typing

from ._get_nth_segment_width import (
    get_nth_segment_bin_count,
    get_nth_segment_bin_width,
)
from ._get_num_segments import get_num_segments


def iter_bin_coords(
    surface_size: int,
) -> typing.Iterable[typing.Tuple[int, int]]:
    """Yields the bin number and within-bin offset of each bin."""
    if surface_size <= 1:
        return

    bin_counter = it.count()
    for segment in range(get_num_segments(surface_size)):
        segment_num_bins = get_nth_segment_bin_count(segment)
        segment_bin_numbers = it.islice(bin_counter, segment_num_bins)

        segment_bin_width = get_nth_segment_bin_width(segment, surface_size)
        segment_bin_offsets = range(segment_bin_width)

        yield from it.product(segment_bin_numbers, segment_bin_offsets)
