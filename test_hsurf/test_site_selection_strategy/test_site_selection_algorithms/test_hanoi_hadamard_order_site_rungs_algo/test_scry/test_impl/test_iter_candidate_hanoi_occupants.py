import itertools as it

from hstrat import _auxiliary_lib as hstrat_aux
import numpy as np
import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_surface_rank_capacity,
)
from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._scry._impl import (
    iter_candidate_hanoi_occupants,
)


@pytest.mark.parametrize("site", range(64))
@pytest.mark.parametrize("rank", range(0, 2**10, 2**8 + 1))
def test_iter_candidate_hanoi_occupants_smoke1(site: int, rank: int):
    # just a smoke test
    res = [*iter_candidate_hanoi_occupants(site, rank)]
    assert len(res)
    assert isinstance(res, list)
    assert all(isinstance(x, int) for x in res)
    assert hstrat_aux.is_nonincreasing(res)


@pytest.mark.parametrize("surface_size", [16, 32, 64])
def test_iter_candidate_hanoi_occupants_smoke2(surface_size: int):
    capacity = get_surface_rank_capacity(surface_size)
    for rank in it.chain(
        range(300),
        map(int, np.linspace(0, capacity, num=100, dtype=int)),
    ):
        {*iter_candidate_hanoi_occupants(0, rank)} == {0}

        for site in range(surface_size):
            assert hstrat_aux.is_nonincreasing(
                iter_candidate_hanoi_occupants(site, rank)
            )


def test_iter_candidate_hanoi_occupants():
    # note use of sets to simplify away value repetition
    assert {*iter_candidate_hanoi_occupants(1, 2)} == {0, 1}
    assert {*iter_candidate_hanoi_occupants(1, 5559)} == {0, 1}
    assert {*iter_candidate_hanoi_occupants(6, 5)} == {0, 2}
    assert {*iter_candidate_hanoi_occupants(5, 5)} == {0, 1}
    assert {*iter_candidate_hanoi_occupants(7, 5)} == {0, 1, 3}
    assert {*iter_candidate_hanoi_occupants(6, 16)} == {0, 2, 6}
    assert {*iter_candidate_hanoi_occupants(5, 16)} == {0, 1, 5}
    assert {*iter_candidate_hanoi_occupants(7, 16)} == {0, 1, 3, 7}
    assert {*iter_candidate_hanoi_occupants(8, 16)} == {0}
    assert {*iter_candidate_hanoi_occupants(9, 16)} == {0, 1}
