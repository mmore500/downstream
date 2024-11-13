import functools
import typing

import polars as pl

from .. import dstream  # noqa: F401
from ._impl._check_downstream_version import check_downstream_version
from ._impl._check_expected_columns import check_expected_columns


def _check_df(df: pl.DataFrame) -> None:
    """Create an empty DataFrame with the expected columns for
    unpack_data_packed, handling edge case of empty input."""
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

    if (
        not df.lazy()
        .filter(pl.col("dstream_T") < pl.col("dstream_S"))
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError("T < S not yet supported")

    if len(df.lazy().select("dstream_algo").unique().limit(2).collect()) > 1:
        raise NotImplementedError("Multiple dstream_algo not yet supported")


def _get_value_type(value_type: str) -> pl.DataType:
    """Convert value_type string arg to Polars DataType object."""
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


def _make_empty(value_type: pl.DataType) -> pl.DataFrame:
    """Create an empty DataFrame with the expected columns for
    unpack_data_packed, handling edge case of empty input."""
    return pl.DataFrame(
        [
            pl.Series(name="data_id", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_algo", values=[], dtype=pl.Utf8),
            pl.Series(name="dstream_Tbar", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_T", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_value", values=[], dtype=value_type),
            pl.Series(
                name="dstream_value_bitsize", values=[], dtype=pl.UInt32
            ),
        ],
    )


def explode_lookup_unpacked(
    df: pl.DataFrame,
    *,
    value_type: typing.Literal["hex", "uint64", "uint32", "uint16", "uint8"],
) -> pl.DataFrame:
    """Explode downstream-curated data from one-buffer-per-row (with each
    buffer containing multiple data items) to one-data-item-per-row, applying
    downstream lookup to identify origin time `Tbar` of each item.

    Parameters
    ----------
    df : pl.DataFrame
        The input DataFrame containing unpacked data with required columns, one
        row per dstream buffer.

        Required schema:

        - 'dstream_algo' : pl.String
            - Name of downstream curation algorithm used
            - e.g., 'dstream.steady_algo'
        - 'dstream_S' : pl.UInt32
            - Capacity of dstream buffer, in number of data items.
        - 'dstream_T' : pl.UInt64
            - Logical time elapsed (number of elapsed data items in stream).
        - 'dstream_storage_hex' : pl.String
            - Raw dstream buffer binary data, containing packed data items.
            - Represented as a hexadecimal string.

        Optional schema:

        - 'data_id' : pl.UInt64
            - Identifier for dstream buffer.
            - If not present, row index will be used as 'data_id'.
        - 'downstream_version' : pl.String
            - Version of downstream library used to curate data items.

        Additional user-defined columns will be forwarded to the output
        DataFrame.

    value_type : {'hex', 'uint64', 'uint32', 'uint16', 'uint8'}
        The desired data type for the 'dstream_value' column in the output
        DataFrame.

        Note that 'hex' is not yet supported.

    Returns
    -------
    pl.DataFrame
        A DataFrame with exploded data and extracted values, one row per data
        item from the input dstream buffers.

        Output schema:

        - 'data_id' : pl.UInt64
            - Identifier of dstream buffer that data item is from.
        - 'dstream_Tbar' : pl.UInt64
            - Logical position of data item in stream (number of prior data
              items).
        - 'dstream_T' : pl.UInt64
            - Logical time elapsed (number of elapsed data items in stream).
        - 'dstream_S' : pl.UInt32
            - Capacity of dstream buffer, in number of data items.
        - 'dstream_value' : pl.String or specified numeric type
            - Data item content, format depends on 'value_type' argument.
        - 'dstream_k' : pl.UInt32
            - Position of data item in dstream buffer.
        - 'dstream_value_bitsize' : pl.UInt32
            - Size of 'dstream_value' in bits.

        User-defined columns and 'downstream_version' will be forwarded from
        the input DataFrame.

    Raises
    ------
    NotImplementedError
        - If 'dstream_value_bitsize' is greater than 64 or equal to 2 or 3.
        - If buffers aren't filled (i.e., 'dstream_T' < 'dstream_S').
        - If multiple dstream algorithms are present in the input DataFrame.
        - If 'value_type' is 'hex'.
    ValeError
        If any of the required columns are missing from the input DataFrame.

    See Also
    --------
    unpack_data_packed :
        Preproccessing step, converts data with downstream buffer and counter
        serialized into a single hexadecimal string into input format for this
        function.
    """
    _check_df(df)
    value_type = _get_value_type(value_type)

    if df.lazy().limit(1).collect().is_empty():
        return _make_empty(value_type)

    df = df.cast(
        {
            "dstream_algo": pl.String,
            "dstream_S": pl.UInt32,
            "dstream_T": pl.UInt64,
            "dstream_storage_hex": pl.String,
        },
    )

    dstream_algo = df.lazy().select("dstream_algo").limit(1).collect().item()
    dstream_algo = eval(dstream_algo)
    do_lookup = functools.lru_cache(dstream_algo.lookup_ingest_times_eager)

    def lookup_ingest_times(cols: pl.Struct) -> typing.List[int]:
        return do_lookup(cols["dstream_S"], cols["dstream_T"])

    column_names = df.lazy().collect_schema().names()
    if "data_id" not in column_names:
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
    if (
        not df.lazy()
        .filter(pl.col("dstream_value_bitsize") > 64)
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError("Value bitsize > 64 not yet supported")
    if (
        not df.lazy()
        .filter(pl.col("dstream_value_bitsize").is_in([2, 3]))
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError("Value bitsize 2 and 3 not yet supported")

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
        .with_row_index("dstream_row_index")
        .with_columns(
            dstream_k=(
                pl.col("dstream_row_index")
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
            ).clip(
                0,
                # 2 ** (pl.col("dstream_value_bitsize") - 1, without overflow
                2
                * (2 ** (pl.col("dstream_value_bitsize") - 1) - 1).cast(
                    pl.UInt64,
                )
                + 1,
            )
        )
        .drop(
            [
                "dstream_algo",
                "dstream_row_index",
                "dstream_storage_bitsize",
                "dstream_storage_hex",
                "dstream_S_cumsum",
                "dstream_value_hexoffset",
                "dstream_value_hexsize",
                "dstream_value_mask",
            ],
        )
        .cast(
            {
                "data_id": pl.UInt64,
                "dstream_k": pl.UInt32,
                "dstream_S": pl.UInt32,
                "dstream_T": pl.UInt64,
                "dstream_Tbar": pl.UInt64,
                "dstream_value": value_type,
                "dstream_value_bitsize": pl.UInt32,
            },
        )
        .collect()
    )
