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
if test_cases.size == 0:
    print("No test cases to run, exiting")
    sys.exit(0)

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

    launcher = {
        "dstream.hybrid_0_steady_1_stretched_2_algo.assign_storage_site": "launch_hybrid_0_steady_1_stretched_2_algo_assign_storage_site",
        "dstream.hybrid_0_steady_1_tilted_2_algo.assign_storage_site": "launch_hybrid_0_steady_1_tilted_2_algo_assign_storage_site",
        "dstream.steady_algo.assign_storage_site": "launch_steady_algo_assign_storage_site",
        "dstream.stretched_algo.assign_storage_site": "launch_stretched_algo_assign_storage_site",
        "dstream.tilted_algo.assign_storage_site": "launch_tilted_algo_assign_storage_site",
    }[args.algo]
    runner.launch(launcher, nonblock=False)

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

with open(args.out, "a") as out:
    for (S, T), result in zip(test_cases, results):
        if result == S + 1:
            print("", file=out)
        elif result == S:
            print("None", file=out)
        else:
            print(result, file=out)

print(f"{results=}")

print("test/client.py complete")
