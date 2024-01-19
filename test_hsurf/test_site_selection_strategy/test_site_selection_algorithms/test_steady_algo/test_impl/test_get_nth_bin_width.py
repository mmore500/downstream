from collections import Counter
import itertools as it

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.steady_algo._impl import (
    get_nth_bin_width,
    get_num_bins,
)


@pytest.mark.parametrize("surface_size", [2**i for i in range(20)])
def test_get_nth_bin_width(surface_size: int):
    bins = [
        get_nth_bin_width(n, surface_size)
        for n in range(get_num_bins(surface_size))
    ]

    if surface_size == 1:  # special case the trivial case
        assert bins == []
        return

    # bin widths should be nonincreasing
    assert all(it.starmap(int.__ge__, it.pairwise(bins)))
    assert bins[0] == surface_size.bit_length() - 1
    assert bins[-1] == 1
    assert sum(bins) == surface_size - 1  # remember: 0th bin reserved

    width_counts = Counter(bins)
    assert [*width_counts] == [*range(surface_size.bit_length() - 1, 0, -1)]
    # check all widths occur as in powers of 2 segments
    assert all(count.bit_count() == 1 for count in width_counts.values())
    # check segment sizes are nonincreasing
    assert all(it.starmap(int.__le__, it.pairwise(width_counts.values())))
    # check first segment is zero
    count_values = iter(width_counts.values())

    # spot check first and last values
    try:
        # first two values should be one
        assert 1 == next(count_values)
        assert 1 == next(count_values)
    except StopIteration:
        pass

    # singletons fill up a quarter of surface
    *__, last = iter(width_counts.values())
    assert last == surface_size // 4 or 1
