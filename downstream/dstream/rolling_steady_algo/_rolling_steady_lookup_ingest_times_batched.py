import numpy as np

from ._rolling_steady_has_ingest_capacity import (
    rolling_steady_has_ingest_capacity,
)
from ._rolling_steady_lookup_ingest_times_eager import (
    rolling_steady_lookup_ingest_times_eager,
)


def rolling_steady_lookup_ingest_times_batched(
    S: int, T: np.ndarray, parallel: bool = True
) -> np.ndarray:
    """Reconstruct ingest times for multiple filled rolling/steady buffers.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two, at least 4.
    T : np.ndarray
        One-dimensional integer array of logical times, each at least S.
    parallel : bool, default True
        Accepted for compatibility. Both settings use a serial fallback.

    Returns
    -------
    np.ndarray
        uint64 array of shape (T.size, S), with sites in physical order.
    """
    T = np.asarray(T)
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T
    assert T.ndim == 1, T.shape
    S = int(S)
    if not rolling_steady_has_ingest_capacity(S, 0):
        raise ValueError(f"Insufficient ingest capacity for {S=}")
    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")
    return np.asarray(
        [rolling_steady_lookup_ingest_times_eager(S, int(t)) for t in T],
        dtype=np.uint64,
    ).reshape((T.size, S))


# lazy loader workaround
lookup_ingest_times_batched = rolling_steady_lookup_ingest_times_batched
