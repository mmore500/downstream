import argparse

from joinem._dataframe_cli import _add_parser_base, _run_dataframe_cli

from .._version import __version__ as downstream_version
from ._demultiplex_data_packed import demultiplex_data_packed


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=False,
        allow_abbrev=False,
        description="If multiplexed (i.e., 'dstream_storage_multiplex' "
        "present), split to one storage buffer per row.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    _add_parser_base(
        parser=parser,
        dfcli_module="downstream.dataframe.demultiplex_data_packed",
        dfcli_version=downstream_version,
    )
    return parser


if __name__ == "__main__":
    parser = _create_parser()
    args, __ = parser.parse_known_args()

    _run_dataframe_cli(
        base_parser=parser,
        output_dataframe_op=demultiplex_data_packed,
    )
