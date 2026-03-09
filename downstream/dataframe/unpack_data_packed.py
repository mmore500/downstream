import argparse
import functools
import sys

from joinem import dataframe_cli

from .._version import __version__ as downstream_version
from ._unpack_data_packed import unpack_data_packed

if __name__ == "__main__":
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument(
        "--mp-context",
        default="spawn",
        type=str,
        help="Multiprocessing start method. " 'Default "spawn".',
    )
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
        description="Unpack data with dstream buffer and counter serialized "
        "into a single hexadecimal data field.",
        module="downstream.dataframe.unpack_data_packed",
        version=downstream_version,
        output_dataframe_op=functools.partial(
            unpack_data_packed,
            mp_context=pre_args.mp_context,
            mp_pool_size=pre_args.mp_pool_size,
        ),
    )
