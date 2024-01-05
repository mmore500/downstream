import pytest

from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_num_incidence_reservations_at_rank,
    get_regime_num_reservations_available,
)


@pytest.mark.parametrize(
    "surface_size",
    [
        16,
        32,
        64,
    ],
)
def test_get_regime_num_reservations_available(surface_size: int):
    # just a smoke test
    focal_rank = hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    assert get_regime_num_reservations_available(
        1, surface_size, focal_rank
    ) == 2 * get_num_incidence_reservations_at_rank(focal_rank, surface_size)
    assert get_regime_num_reservations_available(
        2, surface_size, focal_rank
    ) == 1 * get_num_incidence_reservations_at_rank(focal_rank, surface_size)
