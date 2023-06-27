import itertools as it

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    iter_hanoi_invader_values,
)


def test_iter_hanoi_invader_values():
    assert [*it.islice(iter_hanoi_invader_values(0), 6)] == [
        1,
        2,
        4,
        8,
        16,
        32,
    ]
    assert [*it.islice(iter_hanoi_invader_values(3), 4)] == [7, 11, 19, 35]
    assert [*it.islice(iter_hanoi_invader_values(8), 2)] == [24, 40]
