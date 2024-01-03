import numpy as np
import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.steady_deutsch_alloc_incidence_rungs_algo._impl import (
    get_bin_number_of_position,
    get_nth_bin_position,
    get_nth_bin_width,
)


@pytest.mark.parametrize("surface_size", [2**i for i in range(16)])
def test_get_bin_number_of_position(surface_size: int):
    for position in range(surface_size - 1):
        bin_number = get_bin_number_of_position(position, surface_size)
        bin_position = get_nth_bin_position(bin_number, surface_size)
        bin_width = get_nth_bin_width(bin_number, surface_size)
        assert bin_position <= position < bin_position + bin_width
