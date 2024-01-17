import typing

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo._impl import (
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
def test_get_site_hanoi_value_assigned_epoch0(
    expected: typing.List[int],
):
    assert len(expected).bit_count() == 1  # power of 2
    for rank in range(len(expected) - 1):
        actual = [
            get_site_hanoi_value_assigned(site, rank, len(expected))
            for site in range(len(expected))
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
def test_get_site_hanoi_value_assigned_epoch1(
    expected: typing.List[int],
):
    assert len(expected).bit_count() == 1  # power of 2
    for rank in range(len(expected), 2 * len(expected) - 1):
        actual = [
            get_site_hanoi_value_assigned(site, rank, len(expected))
            for site in range(len(expected))
        ]
        assert expected == actual, rank
