import pytest

from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._enact._impl import (
    has_hanoi_value_filled_first_reservation_layer,
)


@pytest.mark.parametrize(
    "hanoi_value, incidence_thresh, surface_size",
    [
        # surface size 8
        (0, 7, 8),
        (1, 3, 8),
        (2, 1, 8),
        (3, 1, 8),
        (4, 0, 8),
        (5, 0, 8),
        (7, 0, 8),
        # surface size 16
        (0, 15, 16),
        (1, 7, 16),
        (2, 3, 16),
        (3, 3, 16),
        (4, 1, 16),
        (5, 1, 16),
        (7, 1, 16),
        (8, 0, 16),
        (9, 0, 16),
        (15, 0, 16),
    ],
)
def test_has_hanoi_value_filled_first_reservation_layer(
    hanoi_value: int,
    incidence_thresh: int,
    surface_size: int,
):
    rank_thresh = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value,
        incidence_thresh,
    )

    for rank in range(0, 100):
        assert has_hanoi_value_filled_first_reservation_layer(
            hanoi_value,
            surface_size,
            rank,
        ) == (rank >= rank_thresh)
