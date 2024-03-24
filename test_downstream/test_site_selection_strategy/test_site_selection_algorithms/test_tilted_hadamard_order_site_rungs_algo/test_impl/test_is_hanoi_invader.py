from downstream.pylib import hanoi
from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    is_hanoi_invader,
)


def test_is_hanoi_invader():
    assert not is_hanoi_invader(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )
    assert is_hanoi_invader(
        3, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )

    assert not is_hanoi_invader(
        3, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )

    assert not is_hanoi_invader(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )
