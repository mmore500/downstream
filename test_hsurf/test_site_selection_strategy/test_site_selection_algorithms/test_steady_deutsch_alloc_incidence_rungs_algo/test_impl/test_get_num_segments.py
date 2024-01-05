import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.steady_deutsch_alloc_incidence_rungs_algo._impl import (
    get_bin_width_at_position,
    get_nth_bin_width,
    get_num_bins,
    get_num_segments,
)


@pytest.mark.parametrize("surface_size", [2**i for i in range(20)])
def test_get_num_segments(surface_size: int):
    num_bins = get_num_bins(surface_size)
    segments = set(get_nth_bin_width(i, surface_size) for i in range(num_bins))
    assert len(segments) == get_num_segments(surface_size)

    num_positions = surface_size - 1
    segments = set(
        get_bin_width_at_position(i, surface_size)
        for i in range(num_positions)
    )
    assert len(segments) == get_num_segments(surface_size)
