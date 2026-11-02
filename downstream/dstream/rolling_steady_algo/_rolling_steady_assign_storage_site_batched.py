import typing

import numpy as np

from ._rolling_steady_assign_storage_site import (
    rolling_steady_assign_storage_site,
)


def rolling_steady_assign_storage_site_batched(
    S: typing.Union[np.ndarray, int], T: typing.Union[np.ndarray, int]
) -> np.ndarray:
    """Select sites for broadcastable arrays of sizes and logical times.

    Parameters
    ----------
    S : Union[np.ndarray, int]
        Buffer sizes. Each must be a power of two, at least 4.
    T : Union[np.ndarray, int]
        Nonnegative logical times.

    Returns
    -------
    np.ndarray
        Selected sites as uint64, with the broadcast shape of S and T.
        Scalar inputs produce a one-element array, as in steady_algo.

    Notes
    -----
    Serial scalar fallback; this implementation is not vectorized.
    """
    sizes, times = np.broadcast_arrays(np.atleast_1d(S), np.atleast_1d(T))
    assert np.issubdtype(sizes.dtype, np.integer), S
    assert np.issubdtype(times.dtype, np.integer), T
    return np.fromiter(
        (
            rolling_steady_assign_storage_site(int(s), int(t))
            for s, t in zip(sizes.flat, times.flat)
        ),
        dtype=np.uint64,
        count=times.size,
    ).reshape(times.shape)


# lazy loader workaround
assign_storage_site_batched = rolling_steady_assign_storage_site_batched
