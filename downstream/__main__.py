import argparse
import itertools as it
from signal import SIG_BLOCK, SIGPIPE, signal
import sys

from downstream.dstream import steady_algo  # noqa: F401
from downstream.dstream import stretched_algo  # noqa: F401
from downstream.dstream import tilted_algo  # noqa: F401

if __name__ == "__main__":
    signal(SIGPIPE, SIG_BLOCK)

    parser = argparse.ArgumentParser(
        description="Run steady site selection tests"
    )
    parser.add_argument(
        "target",
        help="Function to test (e.g., steady_algo.assign_storage_site)",
    )
    args = parser.parse_args()

    algo = eval(args.target.split(".")[0])
    target = eval(args.target)
    for line in sys.stdin:
        S, T = map(int, line.rstrip().split())
        if algo.has_ingest_capacity(S, T):
            res = target(S, T)
            try:
                print(*it.islice(res, 100))
            except TypeError:
                print(res)
        else:
            print()
