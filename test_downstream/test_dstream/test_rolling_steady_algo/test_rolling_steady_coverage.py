"""Functional coverage checks independent of steady's implementation."""

import random

import pytest

from downstream.dstream import rolling_steady_algo as algo


def _assert_coverage(storage, T):
    S = len(storage)
    m = S // 2
    retained = sorted(t for t in storage if t is not None)
    assert len(retained) == len(set(retained)) == min(S, T)
    assert all(0 <= t < T for t in retained)
    b = max(0, T - m)
    recent = [t for t in retained if t >= b]
    history = [t for t in retained if t < b]

    # Exactly the most recent half-buffer, with no gaps in the rolling window.
    assert recent == list(range(b, T))
    assert len(history) == min(m, b)
    if T < S:
        assert retained == list(range(T))

    # Steady's dyadic coverage contract: retain every completed interval's
    # endpoint at the current spacing. Extra retained points may refine it.
    spacing = 1 << max(0, b.bit_length() - (m.bit_length() - 1))
    assert set(range(spacing - 1, b, spacing)) <= set(history)

    # Count missing items between samples, including the time-zero edge and
    # the boundary with the rolling window. No unobserved run reaches spacing.
    edges = [-1, *history, b]
    gaps = [right - left - 1 for left, right in zip(edges, edges[1:])]
    assert max(gaps) < spacing
    if b >= m:
        # spacing <= 2*b/m: the worst uncovered run is < twice the ideal gap.
        assert max(gaps) * m < 2 * b


@pytest.mark.parametrize("S", [4, 8, 16, 32, 64, 128])
def test_coverage_by_single_write_replay(S):
    storage = [None] * S
    _assert_coverage(storage, 0)
    for T in range(4096):
        site = algo.assign_storage_site(S, T)
        assert 0 <= site < S
        # No lookup, stored timestamps, steady oracle, or relocation is used
        # to maintain this buffer. Arrival numbers are the test payloads.
        storage[site] = T
        _assert_coverage(storage, T + 1)


@pytest.mark.parametrize("S", [4, 16, 64, 256])
def test_coverage_at_large_epoch_boundaries(S):
    m = S // 2
    for bits in (S.bit_length(), 32, 64, 128, 256):
        for offset in (-1, 0, 1, m - 1, m, m + 1):
            # Historical prefix (T-m) crosses a power of two here.
            T = (1 << bits) + m + offset
            storage = list(algo.lookup_ingest_times(S, T))
            _assert_coverage(storage, T)
            for t in range(T, T + S):
                storage[algo.assign_storage_site(S, t)] = t
                _assert_coverage(storage, t + 1)


def test_coverage_at_random_large_times():
    rng = random.Random(20261103)
    for _ in range(256):
        S = 1 << rng.randrange(2, 9)
        T = rng.randrange(S, 1 << rng.randrange(10, 257))
        _assert_coverage(list(algo.lookup_ingest_times(S, T)), T)
