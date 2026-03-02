import argparse
import json
import pathlib
import sys

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
chunkSize = 1024  # number of test cases to run in a single batch

runner = SdkRuntime("out", cmaddr=args.cmaddr, suppress_simfab_trace=True)

runner.load()
runner.run()

results = []
for bounds in tqdm([*mit.pairwise({*range(0, nCases, chunkSize), nCases})]):
    cases_chunk = test_cases[slice(*bounds), :]
    cases_chunk = np.pad(
        cases_chunk,
        ((0, chunkSize), (0, 0)),
        mode="constant",
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

    algo_key = json.loads(
        pathlib.Path(__file__).parent.joinpath("algo_keys.json").read_text(),
    ).index(
        args.algo,
    )
    runner.launch(
        "launch_assign_storage_site", np.uint32(algo_key), nonblock=False
    )

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
