"""Stateless rolling/steady stream curation.

After warm-up, half the S slots hold the latest S/2 samples on the 2**n
grid. The other half hold exactly steady_algo(S/2)'s sample of the older
grid prefix. These are logical groups, not fixed physical partitions.

Selection uses a fixed number of word operations, with no loops, tables,
payload reads, or persistent auxiliary state. Python's arbitrary-width
integer operations themselves are not constant-time in bit complexity.
See rolling_steady.md for the derivation and machine-word assumptions.
"""

from dataclasses import dataclass
import numbers
from typing import List, Optional

import numpy as np

from . import steady_algo


def _select_sample(m: int, k: int) -> int:
    """Select a slot for grid sample k, given S=2*m and m=2**s >= 2."""
    s = m.bit_length() - 1
    x = k + 1
    y = x >> s
    r = x & (m - 1)
    if r:
        lowbit = r & -r
        # odd_part(x) >= m, without a trailing-zero count or multiplication.
        if y >= lowbit:
            return m + r
        h = lowbit.bit_length() - 1
        odd = x >> h
        if odd == 1:
            return (s + 1 - (m >> (h + 1))) % (m + 1)

        b = odd.bit_length()
        w = s + 1 - b
        span = s - h
        divisor = (1 << w) - 1

        # Combine the divisibility and binary-carry stopping conditions.
        threshold = (1 << span) - divisor * ((1 << b) - odd)
        shift = w * ((span + w - max(threshold, 1).bit_length()) // w)
        if shift < span:
            if w == 1:
                # Carry reaches a permanent ring chain. Mask before shifting
                # to avoid constructing a larger virtual stream index.
                return m + ((r & ((m - 1) >> shift)) << shift)
            # Update only the odd part, using the existing carry threshold.
            span -= shift
            odd = (1 << b) + (threshold - (1 << span)) // divisor
            w -= 1
            divisor >>= 1
            shift = w * ((span + w - 1) // w)

        # Evaluate the final normalized index directly. The geometric sum
        # is head + (head-1)/divisor, avoiding a large 2**shift numerator.
        head = 1 << (shift - w)
        y = (odd << (shift - span)) + head + (head - 1) // divisor

    # The remaining m+1 chains are labeled by an invariant epoch phase.
    if y <= m:
        # Evaluate the phase after one virtual forward step. No data moves.
        lowbit = y & -y
        e = lowbit.bit_length() - 1 + s + (y == lowbit)
        z = y << (s + 1 - y.bit_length())
    else:
        v = y - 1
        e = v.bit_length() - 1
        z = v >> (e - s)

    # C(z//2) = z-popcount(z): keep s+1 leading bits instead of s.
    return (e - z + z.bit_count() - 2) % (m + 1)


def _validate(S: int, T: int, n: int) -> None:
    if S < 4 or S & (S - 1):
        raise ValueError("S must be a power of two, at least 4")
    if T < 0 or n < 0:
        raise ValueError("T and n must be nonnegative")


def assign_storage_site(S: int, T: int, n: int = 0) -> Optional[int]:
    """Return the sole slot to overwrite for arrival T, or None to discard.

    T is the zero-based arrival index. S and n are fixed configuration,
    and T is supplied by the caller's usual stream-depth counter.
    """
    _validate(S, T, n)
    if T & ((1 << n) - 1):
        return None
    return _select_sample(S // 2, T >> n)


def lookup_ingest_times(S: int, T: int, n: int = 0) -> List[Optional[int]]:
    """Recover timestamps by physical slot after T raw arrivals, in O(S).

    The returned timestamps are computed output, never retained metadata.
    None marks a slot that has not been written during warm-up.
    """
    _validate(S, T, n)
    m = S // 2
    q = (T + (1 << n) - 1) >> n
    b = max(0, q - m)
    result = [None] * S
    for k in steady_algo.lookup_ingest_times(m, b):
        if k is not None:
            result[_select_sample(m, k)] = k << n
    for k in range(b, q):
        result[_select_sample(m, k)] = k << n
    return result


@dataclass(frozen=True)
class rolling_steady_algo:
    """Steady historical sample plus an evenly spaced rolling sample.

    Parameters
    ----------
    n : int, default 0
        Retain every ``2**n``-th arrival in the rolling sample.

    Notes
    -----
    Requires a power-of-two buffer size S >= 4. The algorithm object is
    immutable and carries only this configuration; the stream depth T remains
    caller-owned as in other dstream algorithms.
    """

    n: int = 0

    def __post_init__(self):
        if not isinstance(self.n, numbers.Integral) or self.n < 0:
            raise ValueError("n must be a nonnegative integer")
        object.__setattr__(self, "n", int(self.n))

    @property
    def __name__(self) -> str:
        return f"rolling_steady_2pow{self.n}_algo"

    def __repr__(self) -> str:
        return f"rolling_steady_algo(n={self.n})"

    def __deepcopy__(self, memo):
        return self

    def get_ingest_capacity(self, S: int) -> Optional[int]:
        return None if S >= 4 and S.bit_count() == 1 else 0

    def has_ingest_capacity(self, S: int, T: int) -> bool:
        assert T >= 0
        return self.get_ingest_capacity(S) is None

    def assign_storage_site(self, S: int, T: int) -> Optional[int]:
        return assign_storage_site(S, T, self.n)

    def assign_storage_site_batched(self, S: int, T) -> np.ndarray:
        times = np.asarray(T)
        return np.fromiter(
            (
                S
                if (site := self.assign_storage_site(S, int(t))) is None
                else site
                for t in times.flat
            ),
            dtype=np.uint64,
            count=times.size,
        ).reshape(times.shape)

    def lookup_ingest_times(self, S: int, T: int):
        return iter(lookup_ingest_times(S, T, self.n))

    def lookup_ingest_times_eager(self, S: int, T: int) -> List[int]:
        result = list(self.lookup_ingest_times(S, T))
        if any(t is None for t in result):
            raise ValueError("T < S not supported for eager lookup")
        return result

    def lookup_ingest_times_batched(
        self, S: int, T: np.ndarray, parallel: bool = True
    ) -> np.ndarray:
        times = np.asarray(T)
        if (times < S).any():
            raise ValueError("T < S not supported for batched lookup")
        return np.asarray(
            [self.lookup_ingest_times_eager(S, int(t)) for t in times.flat],
            dtype=np.uint64,
        ).reshape((times.size, S))

    def has_ingest_capacity_batched(self, S, T) -> np.ndarray:
        times = np.asarray(T)
        return np.full(times.shape, self.get_ingest_capacity(S) is None) & (
            times >= 0
        )
