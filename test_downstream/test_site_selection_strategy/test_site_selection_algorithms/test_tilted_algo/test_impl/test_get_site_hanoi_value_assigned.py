import typing

import pytest

from downstream.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_site_genesis_reservation_index_physical,
    get_site_hanoi_value_assigned,
)


@pytest.mark.parametrize(
    "expected",
    [
        [0, 1, 2, 3, 0, 0, 1, 0],
        [0, 1, 2, 3, 4, 0, 0, 1, 0, 0, 1, 2, 0, 0, 1, 0],
        [0, 1, 2, 0],
    ],
)
@pytest.mark.parametrize(
    "get_grip",
    [get_site_genesis_reservation_index_physical, lambda site, size: None],
)
def test_get_site_hanoi_value_assigned_epoch0(
    expected: typing.List[int], get_grip: typing.Callable
):
    surface_size = len(expected)
    assert surface_size.bit_count() == 1  # power of 2
    for rank in range(surface_size - 1):
        actual = [
            get_site_hanoi_value_assigned(
                site, rank, surface_size, grip=get_grip(site, surface_size)
            )
            for site in range(surface_size)
        ]
        assert expected == actual


@pytest.mark.parametrize(
    "expected",
    [
        [0, 1, 2, 3, 4, 0, 1, 2],
        [0, 1, 2, 3, 4, 5, 0, 1, 2, 0, 1, 2, 3, 0, 1, 2],
        [0, 1, 2, 3],
    ],
)
@pytest.mark.parametrize(
    "get_grip",
    [get_site_genesis_reservation_index_physical, lambda site, size: None],
)
def test_get_site_hanoi_value_assigned_epoch1(
    expected: typing.List[int], get_grip: typing.Callable
):
    surface_size = len(expected)
    assert surface_size.bit_count() == 1  # power of 2
    for rank in range(surface_size, 2 * surface_size - 1):
        actual = [
            get_site_hanoi_value_assigned(
                site, rank, surface_size, grip=get_grip(site, surface_size)
            )
            for site in range(surface_size)
        ]
        assert expected == actual, rank
