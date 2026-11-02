from ..._auxlib._ctz import ctz
from ._rolling_steady_has_ingest_capacity import (
    rolling_steady_has_ingest_capacity,
)


def rolling_steady_assign_storage_site(S: int, T: int) -> int:
    """Site selection algorithm for rolling/steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two, at least 4.
    T : int
        Current logical time (zero-based arrival index).

    Returns
    -------
    int
        Selected site. Every arrival is stored with one payload write.

    Raises
    ------
    ValueError
        If insufficient ingest capacity is available.

    Notes
    -----
    Uses a fixed number of word operations, with no loops, tables, payload
    reads, or persistent auxiliary state. Python's arbitrary-width integer
    operations are not constant-time in bit complexity.
    """
    if not rolling_steady_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")
    return _select_sample(S >> 1, T)


def _select_sample(m: int, k: int) -> int:
    """Select a slot for arrival k, given S=2*m and m=2**s >= 2."""
    s = m.bit_length() - 1
    x = k + 1
    y = x >> s
    r = x & (m - 1)
    if r:
        lowbit = r & -r
        # Permanent ring chains: this path remains active at all stream ages.
        # odd_part(x) >= m, without a trailing-zero count or multiplication.
        if y >= lowbit:
            return m + r

        # Early-time only: odd_part(x) < m and ctz(x) < s imply x < m*m/2.
        # This startup can extend beyond the initial buffer fill at T=S.
        h = lowbit.bit_length() - 1
        odd = x >> h
        if odd == 1:
            # Here -(m+1) < phase < m+1, so one addition replaces modulo.
            phase = s + 1 - (m >> (h + 1))
            return phase + (m + 1) if phase < 0 else phase

        b = odd.bit_length()
        w = s + 1 - b
        span = s - h
        divisor = (1 << w) - 1

        # Combine the divisibility and binary-carry stopping conditions.
        # w and 2**w-1 need not be powers of two, so these startup-only
        # divisions cannot in general be replaced by right shifts.
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
        # Early-time only (k < m*m); absent once k >= m*m.
        # Evaluate the phase after one virtual forward step. No data moves.
        e = ctz(y) + s + (y & (y - 1) == 0)
        z = y << (s + 1 - y.bit_length())
    else:
        v = y - 1
        e = v.bit_length() - 1
        z = v >> (e - s)

    # OEIS A005187 (https://oeis.org/A005187): C(i)=2*i-popcount(i).
    # Hence C(z//2)=z-popcount(z); use s+1 leading bits instead of s.
    # m+1 is not a power of two; masking would change the chain labels.
    return (e - z + z.bit_count() - 2) % (m + 1)


# lazy loader workaround
assign_storage_site = rolling_steady_assign_storage_site
