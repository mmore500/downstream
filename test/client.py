import argparse
import sys
import typing

import more_itertools as mit
import numpy as np
from tqdm import tqdm

from cerebras.sdk.sdk_utils import memcpy_view
from cerebras.sdk.runtime.sdkruntimepybind import (
    SdkRuntime,
    MemcpyDataType,
    MemcpyOrder,
)

def bit_count(n: int) -> int:
    return bin(n).count("1")

def bit_length(n: int) -> int:
    return len(bin(n)) - 2 if n else 0


def ctz(x: int) -> int:
    """Count trailing zeros."""
    return bit_length(x & -x) - 1


def bit_floor(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    mask = 1 << bit_length(n >> 1)
    return n & mask


def steady_get_ingest_capacity(S: int) -> typing.Optional[int]:
    """How many data item ingestions does this algorithm support?

    Returns None if the number of supported ingestions is unlimited.

    See Also
    --------
    has_ingest_capacity : Does this algorithm have the capacity to ingest `n`
    data items?
    """
    surface_size_ok = bit_count(S) == 1 and S > 1
    return None if surface_size_ok else 0


def steady_has_ingest_capacity(S: int, T: int) -> bool:
    """Does this algorithm have the capacity to ingest a data item at logical
    time T?

    Parameters
    ----------
    S : int
        The number of buffer sites available.
    T : int
        Queried logical time.

    Returns
    -------
    bool

    See Also
    --------
    get_ingest_capacity : How many data item ingestions does this algorithm
    support?
    has_ingest_capacity_batched : Numpy-friendly implementation.
    """
    assert T >= 0
    ingest_capacity = steady_get_ingest_capacity(S)
    return ingest_capacity is None or T < ingest_capacity


def steady_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.
    """
    if not steady_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    s = bit_length(S) - 1
    t = bit_length(T) - s  # Current epoch (or negative)
    h = ctz(T + 1)  # Current hanoi value
    if h < t:  # If not a top n(T) hanoi value...
        return None  # ...discard without storing

    i = T >> (h + 1)  # Hanoi value incidence (i.e., num seen)
    if i == 0:  # Special case the 0th bunch
        k_b = 0  # Bunch position
        o = 0  # Within-bunch offset
        w = s + 1  # Segment width
    else:
        j = bit_floor(i) - 1  # Num full-bunch segments
        B = bit_length(j)  # Num full bunches
        k_b = (1 << B) * (s - B + 1)  # Bunch position
        w = h - t + 1  # Segment width
        assert w > 0
        o = w * (i - j - 1)  # Within-bunch offset

    p = h % w  # Within-segment offset
    return k_b + o + p  # Calculate placement site


parser = argparse.ArgumentParser()
parser.add_argument("--name", help="the test compile output dir")
parser.add_argument("--cmaddr", help="IP:port for CS system")
parser.add_argument(
    "--algo",
    help="the algorithm to test",
    default="steady_algo.assign_storage_site",
)
parser.add_argument(
    "--out", help="the output file", default="/tmp/downstream-client.out"
)
args = parser.parse_args()

test_cases = np.array(
    [[*map(int, line.split())] for line in sys.stdin.readlines()],
    dtype=np.uint32,
)
print(f"{test_cases=}")

impl = {
    "steady_algo.assign_storage_site": steady_assign_storage_site,
}[args.algo]

with open(args.out, "w") as f:
    for test_case in test_cases:
        try:
            print(impl(*map(int, test_case)), file=f)
        except ValueError:
            print(file=f)

nCases = test_cases.shape[0]
nRow, nCol = 1, 1  # number of rows, columns, and genome words
wavSize = 32  # number of bits in a wavelet
chunkSize = 2048  # number of test cases to run in a single batch

runner = SdkRuntime("out", cmaddr=args.cmaddr, suppress_simfab_trace=True)

runner.load()
runner.run()

results = []
for bounds in tqdm([*mit.pairwise({*range(0, nCases, chunkSize), nCases})]):
    cases_chunk = test_cases[slice(*bounds), :]
    cases_chunk = np.pad(
        cases_chunk,
        ((0, chunkSize), (0, 0)),
        mode='constant',
        constant_values=0,
    )
    results_chunk = np.zeros(chunkSize, dtype=np.uint32)

    runner.memcpy_h2d(
        runner.get_id("cases"),
        cases_chunk.ravel(),
        0,  # x0
        0,  # y0
        nCol,  # width
        nRow,  # height
        chunkSize * 2,  # num wavelets
        streaming=False,
        data_type=MemcpyDataType.MEMCPY_32BIT,
        order=MemcpyOrder.ROW_MAJOR,
        nonblock=False,
    )

    runner.launch("dolaunch", nonblock=False)

    runner.memcpy_d2h(
        results_chunk,
        runner.get_id("results"),
        0,  # x0
        0,  # y0
        nCol,  # width
        nRow,  # height
        chunkSize,  # num wavelets
        streaming=False,
        data_type=MemcpyDataType.MEMCPY_32BIT,
        order=MemcpyOrder.ROW_MAJOR,
        nonblock=False,
    )
    data = memcpy_view(results_chunk, np.dtype(np.uint32))
    assert len(data) == chunkSize
    results.append(results_chunk)

runner.stop()

results = np.concatenate(results)
print(f"{results=}")

print("test/client.py complete")
