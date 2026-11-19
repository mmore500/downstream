import logging

import polars as pl

from ._impl._check_expected_columns import check_expected_columns


def demultiplex_data_packed(
    df: pl.DataFrame,
    *,
    multiplex: int = 0,
) -> pl.DataFrame:
    """Split multiplexed packed data, with several serialized dstream buffer
    and counter records stored back to back in each 'data_hex' field, into
    one row per record.

    Parameters
    ----------
    df : pl.DataFrame
        The input DataFrame containing packed data, with required column
        'data_hex'.

        Required schema:

        - 'data_hex' : pl.String
            - Raw binary data, with `multiplex` equal-length serialized
              records stored back to back.
            - Represented as a hexadecimal string.

        Other columns, such as dstream bit offsets and widths, describe each
        record (not the whole 'data_hex' field), and are forwarded to every
        record's row.

    multiplex : int, default 0
        Number of records multiplexed into each 'data_hex' field. If 0, data
        is not multiplexed, and `df` is returned unchanged.

    Returns
    -------
    pl.DataFrame
        DataFrame with one row per record, in input row order and then record
        order, with each row's 'data_hex' holding only its own record.

        If `multiplex` is 1 or higher, adds column:

        - 'dstream_multiplex_idx' : pl.UInt32
            - Position of record within its multiplexed 'data_hex' field.

    Raises
    ------
    ValueError
        If `multiplex` is negative, if 'data_hex' is missing, or if any
        'data_hex' length is not divisible by `multiplex`.

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
    check_expected_columns(df, expected_columns=["data_hex"])
    df = df.cast({"data_hex": pl.String})

    record_hexwidth = pl.col("data_hex").str.len_bytes() // multiplex
    misaligned = (
        df.lazy()
        .filter(
            pl.col("data_hex").str.len_bytes() % multiplex != 0,
        )
        .limit(1)
        .collect()
    )
    if not misaligned.is_empty():
        raise ValueError(
            f"data_hex length not divisible by {multiplex=}, "
            f"{misaligned['data_hex'].to_list()=}",
        )

    df = (
        df.with_columns(
            dstream_multiplex_idx=pl.lit(
                [*range(multiplex)], dtype=pl.List(pl.UInt32)
            ),
        )
        .explode("dstream_multiplex_idx")
        .with_columns(
            data_hex=pl.col("data_hex").str.slice(
                pl.col("dstream_multiplex_idx") * record_hexwidth,
                record_hexwidth,
            ),
        )
    )

    logging.info("demultiplex_data_packed complete")
    return df
