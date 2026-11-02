import types

import numpy as np
import pytest

from downstream.dstream import rolling_steady_algo as algo
from downstream.dstream import steady_algo


def test_module_exports():
    assert isinstance(algo, types.ModuleType)
    assert set(dir(algo)) == set(dir(steady_algo))
    assert all(callable(getattr(algo, name)) for name in dir(algo))


@pytest.mark.parametrize("S", range(33))
def test_capacity(S):
    valid = S in (4, 8, 16, 32)
    assert algo.get_ingest_capacity(S) == (None if valid else 0)
    for T in (0, S, 2**128):
        assert algo.has_ingest_capacity(S, T) == valid


@pytest.mark.parametrize("dtype", [np.int32, np.int64, np.uint32, np.uint64])
def test_assign_broadcasting(dtype):
    S = np.array([[4], [8], [32]], dtype=dtype)
    T = np.array([0, 3, 32, 127, 1024], dtype=dtype)
    actual = algo.assign_storage_site_batched(S, T)
    expected = [
        [algo.assign_storage_site(int(s), int(t)) for t in T] for s in S[:, 0]
    ]
    np.testing.assert_array_equal(actual, expected)
    assert actual.dtype == np.uint64
    np.testing.assert_array_equal(
        algo.assign_storage_site_batched(8, 3),
        [algo.assign_storage_site(8, 3)],
    )
    assert algo.assign_storage_site_batched(8, T[:0]).shape == (0,)


def test_capacity_broadcasting():
    S = np.array([[0], [2], [3], [4], [8], [12], [32]])
    T = np.array([0, 10, 1024])
    expected = [
        [algo.has_ingest_capacity(int(s), int(t)) for t in T] for s in S[:, 0]
    ]
    actual = algo.has_ingest_capacity_batched(S, T)
    np.testing.assert_array_equal(actual, expected)
    assert actual.dtype == np.bool_
    with pytest.raises(AssertionError):
        algo.has_ingest_capacity_batched(8, [-1])


@pytest.mark.parametrize("S", [4, 8, 32])
@pytest.mark.parametrize("parallel", [False, True])
def test_lookup_variants(S, parallel):
    times = np.array([S, S + 1, S * S, 2**32], dtype=np.uint64)
    expected = [list(algo.lookup_ingest_times(S, int(T))) for T in times]
    assert [
        algo.lookup_ingest_times_eager(S, int(T)) for T in times
    ] == expected
    actual = algo.lookup_ingest_times_batched(S, times, parallel=parallel)
    np.testing.assert_array_equal(actual, expected)
    assert actual.dtype == np.uint64
    assert algo.lookup_ingest_times_batched(S, times[:0]).shape == (0, S)
    with pytest.raises(ValueError):
        algo.lookup_ingest_times_eager(S, S - 1)
    with pytest.raises(ValueError):
        algo.lookup_ingest_times_batched(S, np.array([S - 1, S]))


def test_batched_uint64_limit():
    times = np.array([2**63, 2**64 - 1], dtype=np.uint64)
    np.testing.assert_array_equal(
        algo.assign_storage_site_batched(16, times),
        [algo.assign_storage_site(16, int(T)) for T in times],
    )
    np.testing.assert_array_equal(
        algo.lookup_ingest_times_batched(16, times),
        [list(algo.lookup_ingest_times(16, int(T))) for T in times],
    )
