from hstrat import _auxiliary_lib as hstrat_auxlib
import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._scry._impl import (
    iter_candidate_hanoi_occupants,
)


@pytest.mark.parametrize("site", range(64))
@pytest.mark.parametrize("rank", range(0, 2**10, 2**8 + 1))
def test_iter_candidate_hanoi_occupants(site: int, rank: int):
    # just a smoke test
    res = [*iter_candidate_hanoi_occupants(site, rank)]
    assert len(res)
    assert isinstance(res, list)
    assert all(isinstance(x, int) for x in res)
    assert hstrat_auxlib.is_nonincreasing(res)
