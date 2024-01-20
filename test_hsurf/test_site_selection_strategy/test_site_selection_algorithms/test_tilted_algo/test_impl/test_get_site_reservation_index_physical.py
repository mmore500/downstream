import typing

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_epoch_rank,
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


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    ],
)
def test_get_site_reservation_index_physical_epoch2(
    expected: typing.List[int],
):
    surface_size = len(expected)
    assert surface_size.bit_count() == 1  # power of 2
    for rank in range(
        get_epoch_rank(2, surface_size),
        get_epoch_rank(3, surface_size) - 1
        if surface_size == 16
        else 2**7 - 1,
    ):
        actual = [
            get_site_reservation_index_physical(site, rank, surface_size)
            for site in range(surface_size)
        ]
        assert expected == actual
