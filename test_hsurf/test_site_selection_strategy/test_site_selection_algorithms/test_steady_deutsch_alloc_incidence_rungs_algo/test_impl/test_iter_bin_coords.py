import itertools as it

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.steady_deutsch_alloc_incidence_rungs_algo._impl import (
    get_bin_number_of_position,
    get_bin_offset_at_position,
    get_num_positions,
    iter_bin_coords,
)


@pytest.mark.parametrize("surface_size", [2**i for i in range(16)])
def test_iter_bin_coords(surface_size: int):
    actual = iter_bin_coords(surface_size)
    expected = (
        (
            get_bin_number_of_position(p, surface_size),
            get_bin_offset_at_position(p, surface_size),
        )
        for p in range(get_num_positions(surface_size))
    )
    assert all(it.starmap(tuple.__eq__, zip(actual, expected, strict=True)))
