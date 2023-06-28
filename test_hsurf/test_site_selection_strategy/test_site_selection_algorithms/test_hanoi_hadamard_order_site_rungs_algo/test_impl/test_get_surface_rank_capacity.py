import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_num_incidence_reservations_at_rank,
    get_surface_rank_capacity,
)


def test_get_surface_rank_capacity():
    assert [
        get_surface_rank_capacity(surface_size) for surface_size in (4, 8, 16)
    ] == [
        # hanoi sequence (1-based):
        15,
        255,
        65535,
    ]


def test_get_surface_rank_capacity_consistency_with_implementation():
    for surface_size in (2**x for x in range(2, 12)):
        # this shouldn't raise an assertion
        get_num_incidence_reservations_at_rank(
            get_surface_rank_capacity(surface_size) - 1,
            surface_size,
        )
        # this should raise an assertion
        with pytest.raises(AssertionError):
            get_num_incidence_reservations_at_rank(
                get_surface_rank_capacity(surface_size),
                surface_size,
            )
