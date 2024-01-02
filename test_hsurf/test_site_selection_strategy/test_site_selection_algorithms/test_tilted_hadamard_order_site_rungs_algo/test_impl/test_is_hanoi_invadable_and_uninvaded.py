from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    is_hanoi_invadable_and_uninvaded,
)


def test_is_hanoi_invadable_and_uninvaded():
    assert is_hanoi_invadable_and_uninvaded(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )
    assert not is_hanoi_invadable_and_uninvaded(
        2, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )
    assert not is_hanoi_invadable_and_uninvaded(
        0, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )
    assert not is_hanoi_invadable_and_uninvaded(
        3, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )
    assert is_hanoi_invadable_and_uninvaded(
        3, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )
    assert not is_hanoi_invadable_and_uninvaded(
        0, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )
    assert is_hanoi_invadable_and_uninvaded(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )
    assert not is_hanoi_invadable_and_uninvaded(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(5, 0)
    )
    assert not is_hanoi_invadable_and_uninvaded(
        5, hanoi.get_index_of_hanoi_value_nth_incidence(5, 0)
    )
