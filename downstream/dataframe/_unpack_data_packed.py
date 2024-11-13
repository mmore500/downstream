import polars as pl

from ._impl._check_expected_columns import check_expected_columns


def _check_df(df: pl.DataFrame) -> None:
    """Validate input DataFrame for unpack_data_packed.

    Raises a ValueError if any of the required columns are missing from the
    DataFrame.
    """
    check_expected_columns(
        df,
        expected_columns=[
            "data_hex",
            "dstream_algo",
            "dstream_storage_bitoffset",
            "dstream_storage_bitwidth",
            "dstream_T_bitoffset",
            "dstream_T_bitwidth",
            "dstream_S",
        ],
    )


def _make_empty() -> pl.DataFrame:
    """Create an empty DataFrame with the expected columns for
    unpack_data_packed, handling edge case of empty input."""
    return pl.DataFrame(
        [
            pl.Series(name="dstream_algo", values=[], dtype=pl.String),
            pl.Series(name="downstream_version", values=[], dtype=pl.String),
            pl.Series(name="dstream_S", values=[], dtype=pl.UInt32),
            pl.Series(name="dstream_T", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_storage_hex", values=[], dtype=pl.String),
        ],
    )


def unpack_data_packed(df: pl.DataFrame) -> pl.DataFrame:
    """Unpack data with dstream buffer and counter serialized into a single
    hexadecimal data field.

    Parameters
    ----------
    df : pl.DataFrame
        The input DataFrame containing packed data with required columns, one
        row per dstream buffer.

        Required schema:
            - 'data_hex' : pl.String
                - Raw binary data, with serialized dstream buffer and counter.
                - Represented as a hexadecimal string.
            - 'dstream_algo' : pl.String
                - Name of downstream curation algorithm used.
                - e.g., 'dstream.steady_algo'
            - 'dstream_storage_bitoffset' : pl.UInt64
                - Position of dstream buffer field in 'data_hex'.
            - 'dstream_storage_bitwidth' : pl.UInt64
                - Size of dstream buffer field in 'data_hex'.
            - 'dstream_T_bitoffset' : pl.UInt64
                - Position of dstream counter field in 'data_hex'.
            - 'dstream_T_bitwidth' : pl.UInt64
                - Size of dstream counter field in 'data_hex'.
            - 'dstream_S' : pl.Uint32
                - Capacity of dstream buffer, in number of data items.

        Optional schema:
            - 'data_id' : pl.UInt64
                - Identifier for dstream buffer.
                - If not present, row index will be used as 'data_id'.
            - 'downstream_version' : pl.String
                - Version of downstream library used to curate data items.

    Returns
    -------
    pl.DataFrame
        Processed DataFrame with unpacked and decoded data fields, one row per
        dstream buffer

        Output schema:
            - 'data_id' : pl.UInt64
                - Identifier for dstream buffer.
                - If not present, row index will be used as 'data_id'.
            - 'dstream_algo' : pl.String
                - Name of downstream curation algorithm used.
                - e.g., 'dstream.steady_algo'
            - 'dstream_T' : pl.UInt64
                - Logical time elapsed (number of elapsed data items in stream).
            - 'dstream_storage_hex' : pl.String
                - Raw dstream buffer binary data, containing packed data items.
                - Represented as a hexadecimal string.

        User-defined columns and 'downstream_version' will be forwarded from
        the input DataFrame.

    Raises
    ------
    NotImplementedError
        If any of the bit offset or bit width columns are not hex-aligned
        (i.e., not multiples of 4 bits).
    ValueError
        If any of the required columns are missing from the input DataFrame.


    See Also
    --------
    downstream.dataframe.explode_lookup_unpacked :
        Explodes unpacked buffers into individual constituent data items.
    """
    _check_df(df)
    if df.lazy().limit(1).collect().is_empty():
        return _make_empty()

    df = df.cast(
        {
            "data_hex": pl.String,
            "dstream_algo": pl.String,
            "dstream_storage_bitoffset": pl.UInt64,
            "dstream_storage_bitwidth": pl.UInt64,
            "dstream_T_bitoffset": pl.UInt64,
            "dstream_T_bitwidth": pl.UInt64,
            "dstream_S": pl.UInt32,
        },
    )

    for col in (
        "dstream_storage_bitoffset",
        "dstream_storage_bitwidth",
        "dstream_T_bitoffset",
        "dstream_T_bitwidth",
    ):
        if (
            not df.lazy()
            .filter((pl.col(col) & pl.lit(0b11) != 0))
            .limit(1)
            .collect()
            .is_empty()
        ):
            raise NotImplementedError(f"{col} not hex-aligned")
        df = df.with_columns(
            (pl.col(col) // pl.lit(4)).alias(col.replace("_bit", "_hex")),
        )

    column_names = df.lazy().collect_schema().names()
    if "data_id" not in column_names:
        df = df.with_row_index("data_id")

    df = df.lazy()

    return (
        df.with_columns(
            dstream_storage_hex=pl.col("data_hex").str.slice(
                pl.col("dstream_storage_hexoffset"),
                length=pl.col("dstream_storage_hexwidth"),
            ),
            dstream_T=pl.col("data_hex")
            .str.slice(
                pl.col("dstream_T_hexoffset"),
                length=pl.col("dstream_T_hexwidth"),
            )
            .str.to_integer(base=16),
        )
        .drop(
            [
                "data_hex",
                "dstream_storage_hexoffset",
                "dstream_storage_hexwidth",
                "dstream_T_hexoffset",
                "dstream_T_hexwidth",
                "dstream_storage_bitoffset",
                "dstream_storage_bitwidth",
                "dstream_T_bitoffset",
                "dstream_T_bitwidth",
            ],
        )
        .cast(
            {
                "data_id": pl.UInt64,
                "dstream_S": pl.UInt32,
                "dstream_T": pl.UInt64,
            },
        )
        .collect()
    )
