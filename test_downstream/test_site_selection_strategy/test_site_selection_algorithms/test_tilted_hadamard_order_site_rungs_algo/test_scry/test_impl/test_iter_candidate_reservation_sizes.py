from hstrat import _auxiliary_lib as hstrat_auxlib
import pytest

from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._scry._impl import (
    iter_candidate_reservation_sizes,
)


@pytest.mark.parametrize("rank", range(0, 2**10, 2**8 + 1))
def test_iter_candidate_reservation_sizes(rank: int):
    # just a smoke test
    res = [*iter_candidate_reservation_sizes(rank)]
    assert len(res)
    assert all(isinstance(x, int) for x in res)
    assert hstrat_auxlib.is_strictly_decreasing(res)
    assert all(x.bit_count() == 1 for x in res)  # ensure perfect powers of 2
