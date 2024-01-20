import typing

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_site_genesis_reservation_index_physical,
)


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 1, 2, 2, 3],
        [0, 0, 0, 0, 0, 1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7],
        [0, 0, 0, 1],
    ],
)
def test_get_site_reservation_index_physical(
    expected: typing.List[int],
):
    assert len(expected).bit_count() == 1  # power of 2
    actual = [
        get_site_genesis_reservation_index_physical(site, len(expected))
        for site in range(len(expected))
    ]
    assert expected == actual
