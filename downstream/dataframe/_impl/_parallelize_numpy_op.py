import functools
import itertools as it
import logging
import os
import typing

import numpy as np

from ..._auxlib._starstarmap import progress_starstarmap


def parallelize_numpy_op(
    chunk_size: int = 16 if "PYTEST_CURRENT_TEST" in os.environ else 2**18,
) -> typing.Callable:
    """Decorator to parallelize processing of a Polars DataFrame by splitting
    it into chunks, processing each chunk in parallel, and then rejoining them.
    """

    def decorator(numpy_op: typing.Callable) -> typing.Callable:
        @functools.wraps(numpy_op)
        def wrapper(*args, **kwargs) -> np.array:
            *args, arr = args

            # Handle empty case without multiprocessing
            if arr.size == 0:
                return numpy_op(*args, arr, **kwargs)

            # Split DataFrame into chunks
            chunk_offsets = range(0, arr.shape[0], chunk_size)
            chunks = (arr[i : i + chunk_size] for i in chunk_offsets)

            logging.info(f"multiprocessing {numpy_op.__name__}...")
            processed_chunks = progress_starstarmap(
                numpy_op,
                zip(*map(it.repeat, args), chunks),
                it.repeat(kwargs),
                total=len(chunk_offsets),
            )

            logging.info("concatenating job chunks...")
            res = np.concatenate(processed_chunks)

            logging.info("completed multiprocessing")
            return res

        return wrapper

    return decorator
