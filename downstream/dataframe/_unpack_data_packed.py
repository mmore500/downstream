import polars as pl

from ._check_expected_columns import check_expected_columns


def _check_df(df: pl.DataFrame) -> None:
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
    return pl.DataFrame(
        {
            "dstream_algo": [],
            "downstream_version": [],
            "dstream_S": [],
            "dstream_T": [],
            "dstream_storage_hex": [],
        },
    )


def unpack_data_packed(df: pl.DataFrame) -> pl.DataFrame:
    _check_df(df)
    if df.is_empty():
        return _make_empty()

    for col in (
        "dstream_storage_bitoffset",
        "dstream_storage_bitwidth",
        "dstream_T_bitoffset",
        "dstream_T_bitwidth",
    ):
        if not df.filter((pl.col(col) & pl.lit(0b11) != 0)).is_empty():
            raise NotImplementedError(f"{col} not hex-aligned")
        df = df.with_columns(
            (pl.col(col) // pl.lit(4)).alias(col.replace("_bit", "_hex")),
        )

    if "data_id" not in df.columns:
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
            .str.to_integer(base=16)
            .cast(pl.UInt64),
        )
        .drop(
            [
                "dstream_storage_hexoffset",
                "dstream_storage_hexwidth",
                "dstream_T_hexoffset",
                "dstream_T_hexwidth",
            ],
        )
        .collect()
    )
