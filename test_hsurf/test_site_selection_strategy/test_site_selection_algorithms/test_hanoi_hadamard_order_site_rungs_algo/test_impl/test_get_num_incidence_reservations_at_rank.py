from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_num_incidence_reservations_at_rank,
)


def test_get_num_incidence_reservations_at_rank():
    assert [
        get_num_incidence_reservations_at_rank(rank, 64) for rank in range(17)
    ] == [
        # hanoi sequence (1-based):
        # fmt: off
        64,  # 1,
        32,  # 2,
        32,  # 1,
        16,  # 3,
        16,  # 1,
        16,  # 2,
        16,  # 1,
        16,  # 4,
        16,  # 1,
        16,  # 2,
        16,  # 1,
        16,  # 3,
        16,  # 1,
        16,  # 2,
        16,  # 1,
        8,   # 5,
        8,
        # 1,
        # fmt: on
    ]
