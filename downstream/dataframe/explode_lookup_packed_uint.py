import argparse
import functools
import logging

from joinem import dataframe_cli

from .._version import __version__ as downstream_version
from ._explode_lookup_packed import explode_lookup_packed


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
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
    )
    parser = _create_parser()
    args, __ = parser.parse_known_args()

    dataframe_cli(
        description="Explode downstream-curated data from hexidecimal "
        "serialization of downstream buffers and counters to "
        "one-data-item-per-row, applying downstream lookup to identify origin "
        "time `Tbar` of each item.",
        module="downstream.dataframe.explode_lookup_packed_uint",
        version=downstream_version,
        output_dataframe_op=functools.partial(
            explode_lookup_packed,
            mp_context=args.mp_context,
            mp_pool_size=args.mp_pool_size,
            value_type="uint64",
        ),
    )
