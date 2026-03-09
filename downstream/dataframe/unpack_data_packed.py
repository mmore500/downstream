import argparse
import functools

from joinem import dataframe_cli

from .._version import __version__ as downstream_version
from ._unpack_data_packed import unpack_data_packed


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--mp-context",
        default="spawn",
        type=str,
        help="Multiprocessing start method. " 'Default "spawn".',
    )
    parser.add_argument(
        "--mp-pool-size",
        default=1,
        type=int,
        help="Number of worker processes for parity computation. "
        "Default 1 (sequential, no multiprocessing overhead).",
    )
    return parser


if __name__ == "__main__":
    parser = _create_parser()
    args, __ = parser.parse_known_args()

    dataframe_cli(
        description="Unpack data with dstream buffer and counter serialized "
        "into a single hexadecimal data field.",
        module="downstream.dataframe.unpack_data_packed",
        version=downstream_version,
        output_dataframe_op=functools.partial(
            unpack_data_packed,
            mp_context=args.mp_context,
            mp_pool_size=args.mp_pool_size,
        ),
    )
