from downstream.pylib import hanoi
from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    is_2x_reservation_eligible,
)


def test_is_2x_reservation_eligible():
    for surface_size in 16, 32, 64:
        assert is_2x_reservation_eligible(
            3,
            surface_size,
            hanoi.get_index_of_hanoi_value_nth_incidence(7, 0) - 1,
        )
        assert not is_2x_reservation_eligible(
            3,
            surface_size,
            hanoi.get_index_of_hanoi_value_nth_incidence(7, 0),
        )

        assert not is_2x_reservation_eligible(
            3,
            surface_size,
            hanoi.get_index_of_hanoi_value_nth_incidence(3, 0),
        )
        assert not is_2x_reservation_eligible(
            3,
            surface_size,
            hanoi.get_index_of_hanoi_value_nth_incidence(4, 0) - 1,
        )
        assert is_2x_reservation_eligible(
            3,
            surface_size,
            hanoi.get_index_of_hanoi_value_nth_incidence(4, 0),
        )
        assert is_2x_reservation_eligible(
            3,
            surface_size,
            hanoi.get_index_of_hanoi_value_nth_incidence(6, 0) - 1,
        )
        assert not is_2x_reservation_eligible(
            2,
            surface_size,
            hanoi.get_index_of_hanoi_value_nth_incidence(6, 0),
        )
