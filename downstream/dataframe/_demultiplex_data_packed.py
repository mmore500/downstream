import logging

import polars as pl

from .._auxlib._choose_pl_engine import choose_pl_engine
from ._impl._check_expected_columns import check_expected_columns


def demultiplex_data_packed(df: pl.DataFrame) -> pl.DataFrame:
    """Split multiplexed packed data, with several dstream buffers stored back
    to back in each 'data_hex' field, into one row per buffer.

    If present, column 'dstream_storage_multiplex' gives each row's number
    of multiplexed buffers. Split rows just adjust storage bit offset, keeping
    original 'data_hex'.

    Parameters
    ----------
    df : pl.DataFrame
        The input DataFrame containing packed data.

        Required schema:

        - 'data_hex' : pl.String
            - Raw binary data, as a hexadecimal string.
        - 'dstream_storage_bitoffset' : pl.UInt64
            - Position of first buffer's storage in 'data_hex'.
        - 'dstream_storage_bitwidth' : pl.UInt64
            - Size of each buffer's storage; buffer `i` begins at
              'dstream_storage_bitoffset' + `i` * 'dstream_storage_bitwidth'.

        Optional schema:

        - 'dstream_storage_multiplex' : pl.UInt32
            - Number of buffers multiplexed into row's 'data_hex' field; 1
              if not multiplexed.
            - If absent, `df` is returned unchanged.

        Other columns, such as dstream T bit offset and width, are shared by
        all buffers, and are forwarded to every buffer's row.

    Returns
    -------
    pl.DataFrame
        DataFrame with one row per packed buffer.

        If 'dstream_storage_multiplex' is present, adds column:

        - 'dstream_storage_multiplex_id' : pl.UInt32
            - Position of buffer within its multiplexed 'data_hex' field.

    Raises
    ------
    ValueError
        If required columns are missing, if any 'dstream_storage_multiplex'
        is less than 1, or if multiplexed buffers exceed
        'data_hex' bounds.

    See Also
    --------
    downstream.dataframe.unpack_data_packed :
        Unpacks packed data, demultiplexing first.
    """
    if "dstream_storage_multiplex" not in df.lazy().collect_schema().names():
        return df

    logging.info("begin demultiplex_data_packed")
    check_expected_columns(
        df,
        expected_columns=[
            "data_hex",
            "dstream_storage_bitoffset",
            "dstream_storage_bitwidth",
        ],
    )
    num_buffers = pl.col("dstream_storage_multiplex").cast(pl.UInt32)
    invalid = (
        df.lazy().filter(num_buffers < 1)
        # in-memory: streaming slow to materialize multi-file scans
        .collect(engine=choose_pl_engine(prefer="in-memory"))
    )
    if not invalid.is_empty():
        raise ValueError(
            "dstream_storage_multiplex must be at least 1, "
            f"{invalid['dstream_storage_multiplex'].to_list()[:10]=}",
        )

    # check if last buffer out of bounds within data_hex
    out_of_bounds = (
        df.lazy().filter(
            pl.col("dstream_storage_bitoffset")
            + num_buffers * pl.col("dstream_storage_bitwidth")
            > pl.col("data_hex").str.len_bytes() * 4,
        )
        # in-memory: streaming slow to materialize multi-file scans
        .collect(engine=choose_pl_engine(prefer="in-memory"))
    )
    if not out_of_bounds.is_empty():
        raise ValueError(
            "multiplexed storage out of bounds, "
            f"{out_of_bounds['data_hex'].str.len_bytes().to_list()[:10]=} "
            f"{out_of_bounds['dstream_storage_bitoffset'].to_list()[:10]=} "
            f"{out_of_bounds['dstream_storage_bitwidth'].to_list()[:10]=} "
            f"{out_of_bounds['dstream_storage_multiplex'].to_list()[:10]=}",
        )

    df = (
        df.with_columns(
            dstream_storage_multiplex_id=pl.int_ranges(
                num_buffers, dtype=pl.UInt32
            ),
        )
        .explode("dstream_storage_multiplex_id")
        .with_columns(
            dstream_storage_bitoffset=pl.col("dstream_storage_bitoffset")
            + pl.col("dstream_storage_multiplex_id")
            * pl.col("dstream_storage_bitwidth"),
        )
    )

    logging.info("demultiplex_data_packed complete")
    return df
