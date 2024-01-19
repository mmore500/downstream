import typing

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
    get_epoch_rank,
    get_site_genesis_reservation_index_physical,
    get_grip_reservation_index_logical,
)


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 2, 1, 1, 3],
        [0, 0, 0, 0, 0, 4, 2, 2, 5, 1, 1, 1, 6, 3, 3, 7],
        [0, 0, 0, 1],
    ],
)
def test_get_grip_reservation_index_logical_epoch0(
    expected: typing.List[int],
):
    surface_size = len(expected)
    assert surface_size.bit_count() == 1  # power of 2
    for rank in range(surface_size - 1):
        actual = [
            get_grip_reservation_index_logical(
                get_site_genesis_reservation_index_physical(site, surface_size),
                rank,
                surface_size,
            )
            for site in range(surface_size)
        ]
        assert expected == actual


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3],
        [0, 0, 0, 0],
    ],
)
def test_get_grip_reservation_index_logical_epoch1(
    expected: typing.List[int],
):
    surface_size = len(expected)
    assert surface_size.bit_count() == 1  # power of 2
    for rank in range(surface_size, 2 * surface_size - 1):
        actual = [
            get_grip_reservation_index_logical(
                get_site_genesis_reservation_index_physical(site, surface_size),
                rank,
                surface_size,
            )
            for site in range(surface_size)
        ]
        assert expected == actual


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    ],
)
def test_get_grip_reservation_index_logical_epoch2(
    expected: typing.List[int],
):
    surface_size = len(expected)
    surface_size = surface_size
    assert surface_size.bit_count() == 1  # power of 2
    for rank in range(
        get_epoch_rank(2, surface_size),
        get_epoch_rank(3, surface_size) - 1
        if surface_size == 16
        else 2**7 - 1,
    ):
        actual = [
            get_grip_reservation_index_logical(
                get_site_genesis_reservation_index_physical(site, surface_size),
                rank,
                surface_size,
            )
            for site in range(surface_size)
        ]
        assert expected == actual
