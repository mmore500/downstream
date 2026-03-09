import argparse
import functools
import logging
import sys

from joinem import dataframe_cli

from .._version import __version__ as downstream_version
from ._explode_lookup_packed import explode_lookup_packed

if __name__ == "__main__":
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
    )
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument(
        "--mp-pool-size",
        default=1,
        type=int,
        help="Number of worker processes for parity computation. "
        "Default 1 (sequential, no multiprocessing overhead).",
    )
    pre_args, remaining = pre_parser.parse_known_args()
    sys.argv = sys.argv[:1] + remaining

    dataframe_cli(
        description="Explode downstream-curated data from hexidecimal "
        "serialization of downstream buffers and counters to "
        "one-data-item-per-row, applying downstream lookup to identify origin "
        "time `Tbar` of each item.",
        module="downstream.dataframe.explode_lookup_packed_uint",
        version=downstream_version,
        output_dataframe_op=functools.partial(
            explode_lookup_packed,
            mp_pool_size=pre_args.mp_pool_size,
            value_type="uint64",
        ),
    )
