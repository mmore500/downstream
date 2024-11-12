import functools
import typing

import polars as pl

from .. import dstream  # noqa: F401
from ._check_downstream_version import check_downstream_version
from ._check_expected_columns import check_expected_columns


def _check_df(df: pl.DataFrame) -> None:
    check_downstream_version(df)
    check_expected_columns(
        df,
        expected_columns=[
            "dstream_algo",
            "dstream_S",
            "dstream_T",
            "dstream_storage_hex",
        ],
    )

    if not df.filter(pl.col("dstream_T") < pl.col("dstream_S")).is_empty():
        raise ValueError("T < S not yet supported")

    if df["dstream_algo"].unique().len() > 1:
        raise ValueError("Multiple dstream_algo not yet supported")


def _get_value_type(value_type: str) -> object:
    value_type = {
        "hex": "hex",
        "uint64": pl.UInt64,
        "uint32": pl.UInt32,
        "uint16": pl.UInt16,
        "uint8": pl.UInt8,
    }.get(value_type, None)
    if value_type is None:
        raise ValueError("Invalid value_type")
    elif value_type == "hex":
        raise NotImplementedError("Hex value_type not yet supported")

    return value_type


def _make_empty() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "data_id": [],
            "dstream_algo": [],
            "dstream_Tbar": [],
            "dstream_T": [],
            "dstream_value": [],
            "dstream_value_bitsize": [],
        },
    )


def explode_lookup_unpacked(
    df: pl.DataFrame,
    value_type: typing.Literal["hex", "uint64", "uint32", "uint16", "uint8"],
) -> pl.DataFrame:
    _check_df(df)
    value_type = _get_value_type(value_type)

    if df.is_empty():
        return _make_empty()

    dstream_algo = eval(df["dstream_algo"].item(0))
    do_lookup = functools.lru_cache(dstream_algo.lookup_ingest_times_eager)

    def lookup_ingest_times(cols: pl.Struct) -> typing.List[int]:
        return do_lookup(cols["dstream_S"], cols["dstream_T"])

    if "data_id" not in df.columns:
        df = df.with_row_index("data_id")

    df = df.with_columns(
        dstream_storage_bitsize=(
            pl.col("dstream_storage_hex").str.len_bytes() * 4
        ),
    ).with_columns(
        dstream_value_bitsize=(
            pl.col("dstream_storage_bitsize") // pl.col("dstream_S")
        ),
    )
    if not df.filter(pl.col("dstream_value_bitsize") > 64).is_empty():
        raise ValueError("Value bitsize > 64 not yet supported")
    if not df.filter(pl.col("dstream_value_bitsize").is_in([2, 3])).is_empty():
        raise ValueError("Value bitsize 2 and 3 not yet supported")

    return (
        df.lazy()
        .with_columns(
            dstream_value_hexsize=(pl.col("dstream_value_bitsize") + 3) // 4,
            dstream_S_cumsum=pl.col("dstream_S").cum_sum(),
            dstream_Tbar=pl.struct(["dstream_S", "dstream_T"]).map_elements(
                lookup_ingest_times,
                return_dtype=pl.List(pl.UInt64),
            ),
        )
        .explode("dstream_Tbar")
        .with_row_index("row")
        .with_columns(
            dstream_k=(
                pl.col("row")
                - pl.col("dstream_S_cumsum")
                + pl.col("dstream_S")
            ),
        )
        .with_columns(
            dstream_value_mask=pl.when(pl.col("dstream_value_bitsize") < 4)
            .then(
                pl.lit(2) ** (pl.col("dstream_k") & 0b11),
            )
            .otherwise(pl.lit(2**64 - 1).cast(pl.UInt64)),
            dstream_value_hexoffset=(
                pl.col("dstream_k") * pl.col("dstream_value_bitsize") // 4
            ),
        )
        .with_columns(
            dstream_value=(
                pl.col("dstream_storage_hex")
                .str.slice(
                    pl.col("dstream_value_hexoffset"),
                    pl.col("dstream_value_hexsize"),
                )
                .str.to_integer(base=16)
                .cast(pl.UInt64)
                & pl.col("dstream_value_mask")
            )
            .clip(
                0,
                # 2 ** (pl.col("dstream_value_bitsize") - 1, without overflow
                2
                * (2 ** (pl.col("dstream_value_bitsize") - 1) - 1).cast(
                    pl.UInt64,
                )
                + 1,
            )
            .cast(value_type),
        )
        .drop(
            [
                "dstream_algo",
                "dstream_storage_bitsize",
                "dstream_value_hexsize",
                "dstream_S_cumsum",
                "dstream_value_mask",
                "dstream_value_hexoffset",
                "dstream_value_bitsize",
            ],
        )
        .collect()
    )
