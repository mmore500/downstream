from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_surface_rank_capacity,
)


def test_get_num_sites_reserved_per_incidence_at_rank():
    assert [
        get_surface_rank_capacity(surface_size) for surface_size in (4, 8, 16)
    ] == [
        # hanoi sequence (1-based):
        15,
        255,
        65535,
    ]
