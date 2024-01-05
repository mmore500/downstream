import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.steady_deutsch_alloc_incidence_rungs_algo._impl import (
    get_bin_number_of_position,
    get_num_bins,
    get_num_positions,
    get_num_segments,
)


@pytest.mark.parametrize("surface_size", [2**i for i in range(20)])
def test_get_num_bins(surface_size: int):
    print(
        [
            get_bin_number_of_position(pos, surface_size)
            for pos in range(get_num_positions(surface_size))
        ]
    )
    expected1 = len(
        set(
            get_bin_number_of_position(pos, surface_size)
            for pos in range(get_num_positions(surface_size))
        ),
    )

    num_segments = get_num_segments(surface_size)
    expected2 = bool(num_segments) + bool(num_segments) * sum(
        2**i for i in range(num_segments - 1)
    )

    assert expected1 == expected2
    assert expected1 == get_num_bins(surface_size)
