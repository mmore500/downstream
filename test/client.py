import argparse
import sys
import typing

import numpy as np

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
parser.add_argument("--algo", help="the algorithm to test")
parser.add_argument("--out", help="the output file")
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

nRow, nCol, nWav = 5, 4, 3  # number of rows, columns, and genome words
wavSize = 32  # number of bits in a wavelet

runner = SdkRuntime("out", cmaddr=args.cmaddr, suppress_simfab_trace=True)

runner.load()
runner.run()
runner.launch("dolaunch", nonblock=False)

memcpy_dtype = MemcpyDataType.MEMCPY_32BIT
out_tensors_u32 = np.zeros((nCol, nRow, nWav), np.uint32)

runner.memcpy_d2h(
    out_tensors_u32,
    runner.get_id("genome"),
    0,  # x0
    0,  # y0
    nCol,  # width
    nRow,  # height
    nWav,  # num wavelets
    streaming=False,
    data_type=memcpy_dtype,
    order=MemcpyOrder.ROW_MAJOR,
    nonblock=False,
)
data = memcpy_view(out_tensors_u32, np.dtype(np.uint32))

genome_bytes = [
    inner.view(np.uint8).tobytes() for outer in data for inner in outer
]
genome_ints = [
    int.from_bytes(genome, byteorder="big") for genome in genome_bytes
]

assert len(genome_ints) == nRow * nCol
sentry_bit = 1 << (nWav * wavSize)
for genome_int in genome_ints:
    print(bin(genome_int | sentry_bit))


genome_hexstrings = [
    np.base_repr(genome_int, base=16).zfill(nWav * wavSize // 4)
    for genome_int in genome_ints
]
for genome_hexstring in genome_hexstrings:
    assert len(genome_hexstring) == nWav * wavSize // 4

    word1_hexstring = genome_hexstring[0:8]
    word1 = int.from_bytes(bytes.fromhex(word1_hexstring), byteorder="little")
    assert word1 == 4294901760

    word2_hexstring = genome_hexstring[8:16]
    word2 = int.from_bytes(bytes.fromhex(word2_hexstring), byteorder="little")
    assert word2 == 4042322160

word3_hexstrings = map(lambda x: x[16:24], genome_hexstrings)
assert len(set(word3_hexstrings)) == nRow * nCol

runner.stop()

# Ensure that the result matches our expectation
print("SUCCESS!")
