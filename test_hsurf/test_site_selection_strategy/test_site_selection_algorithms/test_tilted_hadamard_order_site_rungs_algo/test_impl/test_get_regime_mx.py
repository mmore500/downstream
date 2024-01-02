from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_regime_mx,
)


def test_regime_mx():
    # testing equivalent decision to is_hanoi_invadable_and_uninvaded
    # see test_is_hanoi_invadable_and_uninvaded
    assert (
        get_regime_mx(1, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0))
        == 2
    )
    assert (
        get_regime_mx(2, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0))
        == 1
    )
    assert (
        get_regime_mx(0, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0))
        == 1
    )
    assert (
        get_regime_mx(3, hanoi.get_index_of_hanoi_value_nth_incidence(2, 0))
        == 1
    )
    assert (
        get_regime_mx(3, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0))
        == 2
    )
    assert (
        get_regime_mx(0, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0))
        == 1
    )
    assert (
        get_regime_mx(1, hanoi.get_index_of_hanoi_value_nth_incidence(4, 0))
        == 2
    )
    assert (
        get_regime_mx(1, hanoi.get_index_of_hanoi_value_nth_incidence(5, 0))
        == 1
    )
    assert (
        get_regime_mx(5, hanoi.get_index_of_hanoi_value_nth_incidence(5, 0))
        == 1
    )
