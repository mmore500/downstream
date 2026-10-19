import itertools as it
from random import randrange as rand

from downstream.dstream import discard_algo as algo


def test_discard_site_selection_fuzz():
    testS = it.chain(
        (1 << s for s in range(1, 33)),
        range(0, 65),
    )
    testT = it.chain(range(10**3), (rand(2**128) for _ in range(10**3)))
    for S, T in it.product(testS, testT):
        assert algo.assign_storage_site(S, T) is None


def test_discard_site_selection_zero_size():
    assert algo.assign_storage_site(0, 7) is None
