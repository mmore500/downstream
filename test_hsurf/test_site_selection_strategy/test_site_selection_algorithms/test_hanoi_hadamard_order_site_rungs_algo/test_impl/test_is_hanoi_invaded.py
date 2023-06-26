from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    is_hanoi_invaded,
)


def test_is_hanoi_invaded():
    assert not is_hanoi_invaded(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )
    assert is_hanoi_invaded(
        0, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )
    assert not is_hanoi_invaded(
        3, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0)
    )

    assert not is_hanoi_invaded(
        3, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )
    assert is_hanoi_invaded(
        0, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )
    assert not is_hanoi_invaded(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0)
    )
    assert is_hanoi_invaded(
        1, hanoi.get_index_of_hanoi_value_nth_incidence(5, 0)
    )
