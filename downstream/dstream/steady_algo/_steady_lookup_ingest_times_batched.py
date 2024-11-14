import numpy as np

from ..._auxlib._interleave import interleave
from ._steady_lookup_ingest_times import steady_lookup_impl


def steady_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Ingest time lookup algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : np.ndarray
        Current logical time.

    Returns
    -------
    typing.List[int]
        Ingest time of stored item, if any, at buffer sites in index order.
    """
    T = np.asarray(T)
    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")
    return interleave(tuple(steady_lookup_impl(S, T)))
