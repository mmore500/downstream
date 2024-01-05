import numpy as np
import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.steady_deutsch_alloc_incidence_rungs_algo._impl import (
    get_nth_bin_width,
    get_nth_segment_position,
    get_num_bins,
    get_num_segments,
)


@pytest.mark.parametrize("surface_size", [2**i for i in range(20)])
def test_get_nth_segment_position(surface_size: int):
    bins = [
        get_nth_bin_width(n, surface_size)
        for n in range(get_num_bins(surface_size))
    ]
    bin_positions = [
        0,
        *np.cumsum(bins),
    ]

    for s in range(get_num_segments(surface_size)):
        if s == 0:
            segment_first_bin_number = 0
        else:
            segment_first_bin_number = 1 << (s - 1)
        assert (
            get_nth_segment_position(s, surface_size)
            == bin_positions[segment_first_bin_number]
        )

    # just to double check
    if surface_size > 2:
        assert (
            get_nth_segment_position(
                get_num_segments(surface_size) - 1, surface_size
            )
            == surface_size - surface_size // 4 - 1
        )
