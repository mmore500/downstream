import numpy as np

from ._tilted_lookup_ingest_times import tilted_lookup_impl


def tilted_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Ingest time lookup algorithm for tilted curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : np.ndarray
        One-dimensional array of current logical times.

    Returns
    -------
    np.ndarray
        Ingest time of stored items at buffer sites in index order.

        Two-dimensional array. Each row corresponds to an entry in T. Contains
        S columns, each corresponding to buffer sites.
    """
    T = np.asarray(T)
    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")
    return np.vstack(tuple(tilted_lookup_impl(S, T))).T
