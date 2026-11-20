import logging

import polars as pl

from ._impl._check_expected_columns import check_expected_columns


def demultiplex_data_packed(
    df: pl.DataFrame,
    *,
    multiplex: int = 0,
) -> pl.DataFrame:
    """Split multiplexed packed data, with several dstream buffers stored back
    to back in each 'data_hex' field and sharing other fields (such as the
    dstream counter T), into one row per buffer.

    Each output row keeps the whole 'data_hex' field, with its storage bit
    offset shifted to its own buffer.

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

        Other columns, such as dstream T bit offset and width, are shared by
        all buffers, and are forwarded to every buffer's row.

    multiplex : int, default 0
        Number of buffers multiplexed into each 'data_hex' field. If 0, data
        is not multiplexed, and `df` is returned unchanged.

    Returns
    -------
    pl.DataFrame
        DataFrame with one row per buffer, in input row order and then buffer
        order, with 'dstream_storage_bitoffset' pointing to its buffer.

        If `multiplex` is 1 or higher, adds column:

        - 'dstream_multiplex_idx' : pl.UInt32
            - Position of buffer within its multiplexed 'data_hex' field.

    Raises
    ------
    ValueError
        If `multiplex` is negative, or if required columns are missing.

    See Also
    --------
    downstream.dataframe.unpack_data_packed :
        Unpacks packed data, demultiplexing first if `multiplex` is given.
    """
    if multiplex < 0:
        raise ValueError(f"multiplex must be non-negative, got {multiplex}")
    if multiplex == 0:
        return df

    logging.info(f"begin demultiplex_data_packed with {multiplex=}")
    check_expected_columns(
        df,
        expected_columns=[
            "data_hex",
            "dstream_storage_bitoffset",
            "dstream_storage_bitwidth",
        ],
    )

    df = (
        df.with_columns(
            dstream_multiplex_idx=pl.lit(
                [*range(multiplex)], dtype=pl.List(pl.UInt32)
            ),
        )
        .explode("dstream_multiplex_idx")
        .with_columns(
            dstream_storage_bitoffset=pl.col("dstream_storage_bitoffset")
            + pl.col("dstream_multiplex_idx")
            * pl.col("dstream_storage_bitwidth"),
        )
    )

    logging.info("demultiplex_data_packed complete")
    return df
