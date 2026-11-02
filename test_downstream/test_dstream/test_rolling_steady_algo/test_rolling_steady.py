"""Checks against independent replay of the existing steady algorithm."""

import random

import numpy as np
import pytest

from downstream.dstream import rolling_steady_algo, steady_algo
from downstream.dstream.rolling_steady_algo import assign_storage_site
from downstream.dstream.rolling_steady_algo._rolling_steady_assign_storage_site import (
    _select_sample,
)
from downstream.dsurf import Surface


def lookup_ingest_times(S, T):
    return list(rolling_steady_algo.lookup_ingest_times(S, T))


def _reference_root(m, k):
    """Iterative backward selector, independent of the closed form."""
    s = m.bit_length() - 1
    while k >= 2 * m:
        u = k - m + 1
        residue = u % m
        if residue:
            h = (residue & -residue).bit_length() - 1
            bound = (m << h) - 1
            if u > bound:
                u -= ((u - bound + m - 1) // m) * m
        else:
            e = max(0, u.bit_length() - s)
            u = (u >> e) << e
        k = u + m - 1
        if k < 2 * m:
            break
        h = (u & -u).bit_length() - 1
        odd = u >> h
        w = s + 1 if odd == 1 else s + 1 - odd.bit_length()
        k = (u >> w) - 1
    return k


@pytest.mark.parametrize("S", [4, 8, 16, 32, 64])
def test_replay(S):
    m = S // 2
    storage = [None] * S
    archive = [None] * m
    assert lookup_ingest_times(S, 0) == storage
    for T in range(2048):
        # This is the only operation on the proposed policy's payload buffer.
        storage[assign_storage_site(S, T)] = T

        # Independently simulate steady on the prefix outside the window.
        if T >= m:
            site = steady_algo.assign_storage_site(m, T - m)
            if site is not None:
                archive[site] = T - m

        b = max(0, T + 1 - m)
        recent = set(range(b, T + 1))
        old = set(archive) - {None}
        assert not old & recent
        assert set(storage) - {None} == old | recent
        assert sum(x is not None for x in storage) == min(S, T + 1)
        assert len(old) == min(m, b)
        assert lookup_ingest_times(S, T + 1) == storage


@pytest.mark.parametrize("n", [0, 1, 3, 7])
def test_caller_sampling(n):
    # Raw-time sampling remains a caller concern; T counts sampled arrivals.
    S, d = 16, 1 << n
    surface = Surface(rolling_steady_algo, S)
    for raw_time in range(0, 256 * d, d):
        surface.ingest_one(raw_time)
        assert list(surface) == [
            None if t is None else t * d for t in surface.lookup()
        ]
    assert set(range((256 - S // 2) * d, 256 * d, d)) <= set(surface)


def test_public_surface_interface():
    algo = rolling_steady_algo
    surface = Surface(algo, 16)
    for T in range(256):
        assert surface.ingest_one(T) == algo.assign_storage_site(16, T)
        assert list(surface.lookup()) == list(
            algo.lookup_ingest_times(16, T + 1)
        )

    assert algo.get_ingest_capacity(16) is None
    assert algo.has_ingest_capacity(16, 10**6)
    assert algo.get_ingest_capacity(12) == 0
    assert not algo.has_ingest_capacity(12, 0)
    assert algo.assign_storage_site_batched(16, np.arange(32)).shape == (32,)
    assert algo.lookup_ingest_times_batched(16, np.array([64, 128])).shape == (
        2,
        16,
    )


def test_physical_layout_compatibility():
    # Preserve the original prototype's slot numbering, not only its set.
    assert lookup_ingest_times(16, 64) == [
        23,
        47,
        39,
        3,
        7,
        15,
        31,
        63,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
    ]


def test_warmup_width_boundaries():
    # Exercise carry thresholds and changes of geometric-run width at
    # larger capacities than the full stream replay uses.
    for s in range(1, 17):
        m = 1 << s
        for b in range(1, s + 1):
            odds = {1, (1 << b) - 1, (1 << (b - 1)) + 1}
            for odd in odds:
                for h in range(s):
                    k = (odd << h) - 1
                    assert _select_sample(m, k) == _select_sample(
                        m, _reference_root(m, k)
                    )


def test_large_indices_and_capacity():
    rng = random.Random(20261101)
    for _ in range(10000):
        m = 1 << rng.randrange(1, 65)
        k = rng.randrange(1 << rng.randrange(1, 257))
        site = _select_sample(m, k)
        assert 0 <= site < 2 * m
        assert site == _select_sample(m, _reference_root(m, k))


def test_large_snapshot_uniqueness():
    rng = random.Random(20261102)
    for _ in range(1000):
        S = 1 << rng.randrange(2, 9)
        T = rng.randrange(1 << 64, 1 << 256)
        b = T - S // 2
        expected = {
            k for k in steady_algo.lookup_ingest_times(S // 2, b)
        } | set(range(b, T))
        actual = lookup_ingest_times(S, T)
        assert None not in actual
        assert len(set(actual)) == S
        assert set(actual) == expected


@pytest.mark.parametrize("S", [4, 16, 64, 256])
def test_dyadic_snapshot_boundaries(S):
    m = S // 2
    for extra_bits in (0, 1, 8, 64, 128):
        for offset in (-1, 0, 1, m - 1, m, m + 1):
            T = (1 << (S.bit_length() + extra_bits)) + offset
            storage = lookup_ingest_times(S, T)
            expected = {
                k for k in steady_algo.lookup_ingest_times(m, T - m)
            } | set(range(T - m, T))
            assert len(set(storage)) == S
            assert set(storage) == expected
            storage[assign_storage_site(S, T)] = T
            assert storage == lookup_ingest_times(S, T + 1)


@pytest.mark.parametrize("S", [0, 1, 2, 3, 12])
def test_invalid_capacity(S):
    with pytest.raises(ValueError):
        assign_storage_site(S, 0)
    with pytest.raises(ValueError):
        lookup_ingest_times(S, 0)


def test_negative_time():
    with pytest.raises(AssertionError):
        assign_storage_site(8, -1)
    with pytest.raises(AssertionError):
        lookup_ingest_times(8, -1)
