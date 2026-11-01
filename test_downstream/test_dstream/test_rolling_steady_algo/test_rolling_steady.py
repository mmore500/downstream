"""Checks against independent replay of the existing steady algorithm."""

import random

import numpy as np
import pytest

from downstream.dstream import rolling_steady_algo, steady_algo
from downstream.dstream._rolling_steady_algo import (
    _select_sample,
    assign_storage_site,
    lookup_ingest_times,
)
from downstream.dsurf import Surface


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
@pytest.mark.parametrize("n", [0, 1, 3, 7])
def test_replay(S, n):
    m, d = S // 2, 1 << n
    storage = [None] * S
    archive = [None] * m
    assert lookup_ingest_times(S, 0, n) == storage
    for k in range(1024):
        # This is the only operation on the proposed policy's payload buffer.
        storage[assign_storage_site(S, k * d, n)] = k * d

        # Independently simulate steady on the prefix outside the window.
        if k >= m:
            site = steady_algo.assign_storage_site(m, k - m)
            if site is not None:
                archive[site] = (k - m) * d

        b = max(0, k + 1 - m)
        recent = set(range(b * d, (k + 1) * d, d))
        old = set(archive) - {None}
        assert not old & recent
        assert set(storage) - {None} == old | recent
        assert sum(x is not None for x in storage) == min(S, k + 1)
        assert len(old) == min(m, b)
        for T in {k * d + 1, (k + 1) * d}:
            assert lookup_ingest_times(S, T, n) == storage
            boundary = max(0, T - m * d)
            assert all(boundary <= t < T for t in recent)
            assert all(t < boundary for t in old)


def test_discard_between_grid_points():
    for n in range(1, 7):
        d = 1 << n
        for T in range(5 * d):
            assert (assign_storage_site(16, T, n) is None) == bool(T % d)


def test_public_surface_interface():
    algo = rolling_steady_algo(n=2)
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
    assert lookup_ingest_times(16, 256, 2) == [
        92,
        188,
        156,
        12,
        28,
        60,
        124,
        252,
        220,
        224,
        228,
        232,
        236,
        240,
        244,
        248,
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
        n = rng.randrange(33)
        q = (T + (1 << n) - 1) >> n
        b = q - S // 2
        expected = {
            k << n for k in steady_algo.lookup_ingest_times(S // 2, b)
        } | {k << n for k in range(b, q)}
        actual = lookup_ingest_times(S, T, n)
        assert None not in actual
        assert len(set(actual)) == S
        assert set(actual) == expected


@pytest.mark.parametrize("S", [4, 16, 64, 256])
@pytest.mark.parametrize("n", [0, 3])
def test_dyadic_snapshot_boundaries(S, n):
    m = S // 2
    for extra_bits in (0, 1, 8, 64, 128):
        for offset in (-1, 0, 1, m - 1, m, m + 1):
            q = (1 << (S.bit_length() + extra_bits)) + offset
            T = q << n
            storage = lookup_ingest_times(S, T, n)
            expected = {
                k << n for k in steady_algo.lookup_ingest_times(m, q - m)
            } | {k << n for k in range(q - m, q)}
            assert len(set(storage)) == S
            assert set(storage) == expected
            storage[assign_storage_site(S, T, n)] = T
            assert storage == lookup_ingest_times(S, T + 1, n)


@pytest.mark.parametrize(
    "S,T,n", [(2, 0, 0), (12, 0, 0), (8, -1, 0), (8, 0, -1)]
)
def test_invalid_arguments(S, T, n):
    with pytest.raises(ValueError):
        assign_storage_site(S, T, n)
    with pytest.raises(ValueError):
        lookup_ingest_times(S, T, n)
