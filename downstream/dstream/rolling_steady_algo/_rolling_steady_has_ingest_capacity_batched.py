import typing

import numpy as np


def rolling_steady_has_ingest_capacity_batched(
    S: typing.Union[int, np.ndarray],
    T: typing.Union[int, np.ndarray],
) -> np.ndarray:
    """Check capacity for broadcastable buffer sizes and logical times.

    Returns a boolean array with the broadcast shape of S and T. Buffer
    sizes must be powers of two, at least 4; logical times must be nonnegative.
    """
    S, T = np.asarray(S), np.asarray(T)
    assert (T >= 0).all()
    surface_size_ok = np.logical_and(np.bitwise_count(S) == 1, S >= 4)
    return surface_size_ok + np.zeros_like(T, dtype=bool)


# lazy loader workaround
has_ingest_capacity_batched = rolling_steady_has_ingest_capacity_batched
