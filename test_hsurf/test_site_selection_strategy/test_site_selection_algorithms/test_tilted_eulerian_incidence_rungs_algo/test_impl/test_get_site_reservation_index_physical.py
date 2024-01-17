import typing

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    get_site_reservation_index_physical,
)


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 1, 2, 2, 3],
        [0, 0, 0, 0, 0, 1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7],
        [0, 0, 0, 1],
    ],
)
def test_get_site_reservation_index_physical_epoch0(
    expected: typing.List[int],
):
    assert len(expected).bit_count() == 1  # power of 2
    for rank in range(len(expected) - 1):
        actual = [
            get_site_reservation_index_physical(site, rank, len(expected))
            for site in range(len(expected))
        ]
        assert expected == actual


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3],
        [0, 0, 0, 0],
    ],
)
def test_get_site_reservation_index_physical_epoch1(
    expected: typing.List[int],
):
    assert len(expected).bit_count() == 1  # power of 2
    for rank in range(len(expected), 2 * len(expected) - 1):
        actual = [
            get_site_reservation_index_physical(site, rank, len(expected))
            for site in range(len(expected))
        ]
        assert expected == actual
