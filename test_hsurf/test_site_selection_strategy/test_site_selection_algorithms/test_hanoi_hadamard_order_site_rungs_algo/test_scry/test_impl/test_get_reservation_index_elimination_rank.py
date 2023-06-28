import typing

import pytest

from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_num_incidence_reservations_at_rank,
)
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._scry._impl import (
    get_reservation_index_elimination_rank,
)


@pytest.mark.parametrize("hanoi_value", range(4))
@pytest.mark.parametrize("surface_size", [8, 32])
def test_get_reservation_index_elimination_rank(
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
