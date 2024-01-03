from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_num_sites_reserved_per_incidence_at_rank,
)


def test_get_num_sites_reserved_per_incidence_at_rank():
    assert [
        get_num_sites_reserved_per_incidence_at_rank(rank)
        for rank in range(17)
    ] == [
        # hanoi sequence (1-based):
        1,  # 1,
        2,  # 2,
        2,  # 1,
        4,  # 3,
        4,  # 1,
        4,  # 2,
        4,  # 1,
        4,  # 4,
        4,  # 1,
        4,  # 2,
        4,  # 1,
        4,  # 3,
        4,  # 1,
        4,  # 2,
        4,  # 1,
        8,  # 5,
        8,  # 1,
    ]
