import numpy as np
import pytest

from downstream.dstream import stretched_algo as algo


@pytest.mark.parametrize("s", range(1, 12))
def test_stretched_time_lookup_batched_against_site_selection(s: int):
    S = 1 << s
    T_max = min(1 << 17 - s, 2**S - 1)
    expected = [None] * S

    expecteds = []
    for T in range(T_max):
        if T >= S:
            expecteds.extend(expected)

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T

    actual = algo.lookup_ingest_times_batched(S, np.arange(S, T_max)).ravel()
    np.testing.assert_array_equal(expecteds, actual)


@pytest.mark.parametrize("s", range(1, 12))
def test_stretched_time_lookup_batched_empty(s: int):
    S = 1 << s

    res = algo.lookup_ingest_times_batched(S, np.array([], dtype=int))
    assert res.size == 0
