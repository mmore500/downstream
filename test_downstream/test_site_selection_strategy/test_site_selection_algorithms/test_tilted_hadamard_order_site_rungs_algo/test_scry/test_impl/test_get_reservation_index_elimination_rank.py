import typing

import pytest

from downstream.pylib import hanoi
from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_num_incidence_reservations_at_rank,
)
from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._scry._impl import (
    get_reservation_index_elimination_rank,
)

from ._impl import make_num_reservations_provided_df


@pytest.mark.parametrize("hanoi_value", range(4))
@pytest.mark.parametrize("surface_size", [8, 32])
def test_get_reservation_index_elimination_rank_smoke(
    hanoi_value: int, surface_size: int
):
    # just a smoke test
    first_layer_size = get_num_incidence_reservations_at_rank(
        hanoi.get_index_of_hanoi_value_nth_incidence(hanoi_value, 0),
        surface_size,
    )

    for reservation_index in range(first_layer_size):
        actual_result = get_reservation_index_elimination_rank(
            hanoi_value, reservation_index, surface_size
        )
        assert isinstance(actual_result, typing.Optional[int])


@pytest.mark.parametrize(
    "surface_size",
    [
        16,
        pytest.param(32, marks=pytest.mark.heavy),
        pytest.param(64, marks=pytest.mark.heavy),
    ],
)
def test_get_reservation_index_elimination_rank(surface_size: int):
    # actual test
    nrp_df = make_num_reservations_provided_df(surface_size)

    for hanoi_value, hv_df in nrp_df.groupby("hanoi value"):
        assert hv_df["num reservations provided"].is_monotonic_decreasing
        max_reservations_provided = hv_df["num reservations provided"].max()
        expected = None
        actual = get_reservation_index_elimination_rank(
            hanoi_value=hanoi_value,
            reservation_index=max_reservations_provided,
            surface_size=surface_size,
        )
        assert expected == actual, {
            "expected": expected,
            "actual": actual,
            "hanoi value": hanoi_value,
            "reservation index": max_reservations_provided,
            "surface size": surface_size,
        }
        max_covered_rank = hv_df["rank"].max()

        for nrp, nrp_df_ in hv_df.groupby("num reservations provided"):
            assert nrp
            reservation_index = nrp - 1
            expected_last = nrp_df_["rank"].max()
            actual_last = (
                get_reservation_index_elimination_rank(
                    hanoi_value=hanoi_value,
                    reservation_index=reservation_index,
                    surface_size=surface_size,
                )
                - 1
            )
            assert actual_last >= 0
            if (
                expected_last < max_covered_rank
            ):  # skip where coverage goes off end of sampled ranks
                assert expected_last == actual_last, {
                    "expected last": expected_last,
                    "actual last": actual_last,
                    "hanoi value": hanoi_value,
                    "reservation index": reservation_index,
                    "surface size": surface_size,
                }
