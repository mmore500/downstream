import pytest

from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._enact._impl import (
    get_upcoming_hanoi_invasion_value,
)


@pytest.mark.parametrize(
    "focal_hv, reference_hv, reference_incidence, expected_invader_hv",
    [
        # hanoi value 0
        {
            "focal_hv": 0,
            "reference_hv": 0,
            "reference_incidence": 0,
            "expected_invader_hv": 1,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 0,
            "reference_incidence": 1,
            "expected_invader_hv": 2,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 1,
            "reference_incidence": 0,
            "expected_invader_hv": 2,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 3,
            "reference_incidence": 0,
            "expected_invader_hv": 4,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 3,
            "reference_incidence": 1,
            "expected_invader_hv": 8,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 5,
            "reference_incidence": 0,
            "expected_invader_hv": 8,
        }.values(),
        # hanoi value 1
        {
            "focal_hv": 1,
            "reference_hv": 0,
            "reference_incidence": 1,
            "expected_invader_hv": 3,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 1,
            "reference_incidence": 0,
            "expected_invader_hv": 3,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 3,
            "reference_incidence": 0,
            "expected_invader_hv": 5,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 3,
            "reference_incidence": 1,
            "expected_invader_hv": 5,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 5,
            "reference_incidence": 0,
            "expected_invader_hv": 9,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 7,
            "reference_incidence": 0,
            "expected_invader_hv": 9,
        }.values(),
        # hanoi value 7
        {
            "focal_hv": 7,
            "reference_hv": 0,
            "reference_incidence": 0,
            "expected_invader_hv": 15,
        }.values(),
        {
            "focal_hv": 7,
            "reference_hv": 1,
            "reference_incidence": 3,
            "expected_invader_hv": 15,
        }.values(),
        {
            "focal_hv": 7,
            "reference_hv": 6,
            "reference_incidence": 0,
            "expected_invader_hv": 15,
        }.values(),
        {
            "focal_hv": 7,
            "reference_hv": 7,
            "reference_incidence": 0,
            "expected_invader_hv": 15,
        }.values(),
        {
            "focal_hv": 7,
            "reference_hv": 14,
            "reference_incidence": 0,
            "expected_invader_hv": 15,
        }.values(),
        {
            "focal_hv": 7,
            "reference_hv": 15,
            "reference_incidence": 0,
            "expected_invader_hv": 23,
        }.values(),
        {
            "focal_hv": 7,
            "reference_hv": 23,
            "reference_incidence": 0,
            "expected_invader_hv": 39,
        }.values(),
        # hanoi value 8
        {
            "focal_hv": 8,
            "reference_hv": 0,
            "reference_incidence": 0,
            "expected_invader_hv": 24,
        }.values(),
        {
            "focal_hv": 8,
            "reference_hv": 23,
            "reference_incidence": 0,
            "expected_invader_hv": 24,
        }.values(),
        {
            "focal_hv": 8,
            "reference_hv": 24,
            "reference_incidence": 0,
            "expected_invader_hv": 40,
        }.values(),
    ],
)
def test_get_upcoming_hanoi_invasion_value(
    focal_hv: int,
    reference_hv: int,
    reference_incidence: int,
    expected_invader_hv: int,
):
    reference_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
        reference_hv,
        reference_incidence,
    )

    assert (
        get_upcoming_hanoi_invasion_value(
            focal_hv,
            reference_rank,
        )
        == expected_invader_hv
    )


@pytest.mark.parametrize(
    "focal_hv, reference_hv, reference_incidence, expected_invader_hv",
    [
        # hanoi value 0
        {
            "focal_hv": 0,
            "reference_hv": 0,
            "reference_incidence": 1,
            "expected_invader_hv": 2,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 1,
            "reference_incidence": 0,
            "expected_invader_hv": 1,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 3,
            "reference_incidence": 0,
            "expected_invader_hv": 4,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 4,
            "reference_incidence": 0,
            "expected_invader_hv": 4,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 3,
            "reference_incidence": 1,
            "expected_invader_hv": 8,
        }.values(),
        {
            "focal_hv": 0,
            "reference_hv": 5,
            "reference_incidence": 0,
            "expected_invader_hv": 8,
        }.values(),
        # hanoi value 1
        {
            "focal_hv": 1,
            "reference_hv": 0,
            "reference_incidence": 1,
            "expected_invader_hv": 3,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 1,
            "reference_incidence": 0,
            "expected_invader_hv": 3,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 3,
            "reference_incidence": 0,
            "expected_invader_hv": 3,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 3,
            "reference_incidence": 1,
            "expected_invader_hv": 5,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 5,
            "reference_incidence": 0,
            "expected_invader_hv": 5,
        }.values(),
        {
            "focal_hv": 1,
            "reference_hv": 7,
            "reference_incidence": 0,
            "expected_invader_hv": 9,
        }.values(),
    ],
)
def test_get_upcoming_hanoi_invasion_value__rank_minus_one(
    focal_hv: int,
    reference_hv: int,
    reference_incidence: int,
    expected_invader_hv: int,
):
    reference_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
        reference_hv,
        reference_incidence,
    )

    assert (
        get_upcoming_hanoi_invasion_value(
            focal_hv,
            reference_rank - 1,
        )
        == expected_invader_hv
    )
