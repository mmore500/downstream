import pytest

from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_num_reservations_provided,
)
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._scry._impl import (
    calc_rank_of_deposited_hanoi_value,
)


@pytest.mark.parametrize("hanoi_value", range(4))
@pytest.mark.parametrize("surface_size", [8, 32])
@pytest.mark.parametrize("focal_rank", range(128))
def test_calc_rank_of_deposited_hanoi_value_smoke(
    hanoi_value: int, surface_size: int, focal_rank: int
):
    # just a smoke test
    num_reservations_provided = get_num_reservations_provided(
        hanoi_value,
        surface_size,
        focal_rank,
    )

    for reservation_index in range(num_reservations_provided):
        hanoi_count = hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value, focal_rank
        )
        if hanoi_count > reservation_index:
            actual_result = calc_rank_of_deposited_hanoi_value(
                hanoi_value, reservation_index, surface_size, focal_rank
            )
            assert isinstance(actual_result, int)
            assert (
                hanoi.get_index_of_hanoi_value_nth_incidence(
                    hanoi_value,
                    reservation_index,
                )
                <= actual_result
                <= focal_rank
            )
