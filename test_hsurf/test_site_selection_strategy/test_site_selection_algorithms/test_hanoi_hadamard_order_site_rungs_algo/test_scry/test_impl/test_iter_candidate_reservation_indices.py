from hstrat import _auxiliary_lib as hstrat_aux
import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._scry._impl import (
    iter_candidate_reservation_indices,
)


@pytest.mark.parametrize("surface_size", [16, 32, 64])
@pytest.mark.parametrize("rank", range(0, 2**10, 2**8 + 1))
def test_iter_candidate_reservation_indices_smoke(
    surface_size: int, rank: int
):
    for site in range(surface_size):
        # just a smoke test
        res = [*iter_candidate_reservation_indices(site, surface_size, rank)]
        if site == 0:
            assert set(res) == {0}
        if rank == 0:
            assert len(res) == 1

        assert len(res)
        assert all(isinstance(x, int) for x in res)
        assert all(0 <= x < surface_size for x in res)
        assert hstrat_aux.is_nondecreasing(res)
