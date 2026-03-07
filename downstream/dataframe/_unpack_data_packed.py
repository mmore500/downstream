import logging
import pathlib
import typing
import uuid
import warnings

import numpy as np
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


def _enforce_hex_aligned(df: pl.DataFrame, col: str) -> None:
    """Raise NotImplementedError if column is not hex-aligned (i.e., not a
    multiple of 4 bits)."""
    if (
        not df.lazy()
        .filter((pl.col(col) & pl.lit(0b11) != 0))
        .limit(1)
        .collect()
        .is_empty()
    ):
        raise NotImplementedError(f"{col} not hex-aligned")


def _make_empty() -> pl.DataFrame:
    """Create an empty DataFrame with the expected columns for
    unpack_data_packed, handling edge case of empty input."""
    return pl.DataFrame(
        [
            pl.Series(name="dstream_algo", values=[], dtype=pl.String),
            pl.Series(name="dstream_data_id", values=[], dtype=pl.UInt64),
            pl.Series(name="downstream_version", values=[], dtype=pl.String),
            pl.Series(name="dstream_S", values=[], dtype=pl.UInt32),
            pl.Series(name="dstream_T", values=[], dtype=pl.UInt64),
            pl.Series(name="dstream_storage_hex", values=[], dtype=pl.String),
        ],
    )


def _calculate_offsets(df: pl.DataFrame) -> pl.DataFrame:
    for col in (
        "dstream_storage_bitoffset",
        "dstream_storage_bitwidth",
        "dstream_T_bitoffset",
        "dstream_T_bitwidth",
    ):
        _enforce_hex_aligned(df, col)
        df = df.with_columns(
            **{col.replace("_bit", "_hex"): np.right_shift(pl.col(col), 2)},
        )

    for what in "dstream_storage", "dstream_T":
        hexoffset = f"{what}_hexoffset"
        hexwidth = f"{what}_hexwidth"
        out_of_bounds = (
            df.lazy()
            .filter(
                pl.col(hexoffset) + pl.col(hexwidth)
                > pl.col("data_hex").str.len_bytes(),
            )
            .collect()
        )
        if not out_of_bounds.is_empty():
            raise ValueError(
                f"{what} offset/width out of bounds, "
                f"{out_of_bounds['data_hex'].str.len_bytes().to_list()[:10]=} "
                f"{out_of_bounds[hexoffset].to_list()[:10]=} "
                f"{out_of_bounds[hexwidth].to_list()[:10]=} "
                f"{out_of_bounds[:10]=}",
            )

    return df


def _extract_from_data_hex(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.lazy()
        .with_columns(
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
        .collect()
    )


def _perform_validations(
    df: pl.DataFrame,
    col_name: str,
) -> pl.DataFrame:
    validator_strs = (
        df.select(pl.col(col_name))
        .to_series()
        .unique()
        .drop_nulls()
        .to_list()
    )
    validator_strs = [s for s in validator_strs if s]
    num_validators = len(validator_strs)

    for validator in validator_strs:
        validation_expr = eval(validator, {"pl": pl})
        group = df.filter(pl.col(col_name) == validator)
        validation_result = group.select(validation_expr).to_series()
        if not validation_result.all():
            err_msg = f"{col_name} `{validator}` failed"
            logging.error(err_msg)
            failed_rows = group.filter(~validation_result)
            logging.error(failed_rows.glimpse(return_as_string=True))
            for dump_path in (
                pathlib.Path.home()
                / f"downstream_validation_fail_{uuid.uuid4()}.pqt",
                f"/tmp/downstream_validation_fail_{uuid.uuid4()}.pqt",  # nosec B108
            ):
                try:
                    failed_rows.write_parquet(dump_path)
                    logging.error(f"failing rows dumped to {dump_path}")
                    break
                except Exception as e:
                    logging.error(
                        f"failed to dump rows to {dump_path}: {e}",
                    )
            raise ValueError(err_msg)

    df = df.drop(col_name)
    logging.info(f" - {num_validators} validation(s) passed!")

    return df


def _apply_filters(
    df: pl.DataFrame,
    col_name: str,
) -> pl.DataFrame:
    num_before = len(df)
    filter_strs = (
        df.select(pl.col(col_name))
        .to_series()
        .unique()
        .drop_nulls()
        .to_list()
    )
    filter_strs = [s for s in filter_strs if s]
    num_filters = len(filter_strs)

    combined_expr = pl.lit(True)
    for filter_expr_str in filter_strs:
        filter_expr = eval(filter_expr_str, {"pl": pl})
        match_rows = pl.col(col_name) == filter_expr_str
        # for rows matching this filter group, apply the filter;
        # for other rows, pass through
        combined_expr = combined_expr & pl.when(match_rows).then(
            filter_expr,
        ).otherwise(True)

    df_out = df.lazy().filter(combined_expr).collect().drop(col_name)

    # per-group logging
    for filter_expr_str in filter_strs:
        filter_expr = eval(filter_expr_str, {"pl": pl})
        group = df.filter(pl.col(col_name) == filter_expr_str)
        filter_result = group.select(filter_expr).to_series()
        num_kept = filter_result.sum()
        num_dropped = len(group) - num_kept
        logging.info(
            f"   - filter `{filter_expr_str}`: "
            f"{num_dropped} dropped, {num_kept} kept "
            f"from {len(group)} rows",
        )

    num_after = len(df_out)
    num_filtered = num_before - num_after
    logging.info(
        f" - {num_filters} filter(s) applied, "
        f"{num_filtered} dropped and {num_after} kept "
        f"from {num_before} rows!",
    )

    return df_out


def _drop_excluded_rows(df: pl.DataFrame) -> pl.DataFrame:
    for col_name in (
        "downstream_filter_exploded",
        "downstream_validate_exploded",
    ):
        has_dropped = (
            col_name in df
            and df.select(
                (pl.col(col_name).str.len_bytes() > 0)
                & pl.col("downstream_exclude_unpacked")
            )
            .to_series()
            .any()
        )
        if has_dropped:
            warnings.warn(
                f"row(s) with both `{col_name}` "
                "and `downstream_exclude_unpacked` detected,"
                "but these rows will be dropped before validation",
            )

    kept = pl.col("downstream_exclude_unpacked").not_().fill_null(True)
    num_before = len(df)
    df = df.filter(kept).drop("downstream_exclude_unpacked")
    num_after = len(df)
    num_dropped = num_before - num_after
    logging.info(
        f" - {num_dropped} dropped and {num_after} kept "
        f"from {num_before} rows!",
    )
    return df


def _finalize_result_schema(
    df: pl.DataFrame, result_schema: str
) -> pl.DataFrame:
    try:
        df = {
            "coerce": lambda df: df.cast(
                {
                    "dstream_data_id": pl.UInt64,
                    "dstream_S": pl.UInt32,
                    "dstream_T": pl.UInt64,
                    "dstream_storage_hex": pl.String,
                },
            ),
            "relax": lambda df: df,
            "shrink": lambda df: df.select(pl.all().shrink_dtype()),
        }[result_schema](df)
    except KeyError:
        raise ValueError(f"Invalid arg {result_schema} for result_schema")
    return df


def unpack_data_packed(
    df: pl.DataFrame,
    *,
    result_schema: typing.Literal["coerce", "relax", "shrink"] = "coerce",
) -> pl.DataFrame:
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
        - 'dstream_algo' : pl.Categorical
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
        - 'dstream_S' : pl.UInt32
            - Capacity of dstream buffer, in number of data items.

        Optional schema:

        - 'downstream_exclude_exploded' : pl.Boolean
            - Should row be dropped after exploding unpacked data?
        - 'downstream_exclude_unpacked' : pl.Boolean
            - Should row be dropped after unpacking packed data?
        - 'downstream_filter_exploded' : pl.String, polars expression
            - Polars expression to filter exploded data; non-matching rows
            are dropped.
        - 'downstream_filter_packed' : pl.String, polars expression
            - Polars expression to filter packed data; non-matching rows
            are dropped.
        - 'downstream_filter_unpacked' : pl.String, polars expression
            - Polars expression to filter unpacked data; non-matching rows
            are dropped.
        - 'dstream_T_dilation' : pl.UInt32
            - Dilation factor applied to T counter, if any; supports scenario
            where data items are ingested every `dstream_T_dilation`th counter
            step (default 1).
        - 'downstream_validate_exploded' : pl.String, polars expression
            - Polars expression to validate exploded data.
        - 'downstream_validate_packed' : pl.String, polars expression
            - Polars expression to validate packed data.
        - 'downstream_validate_unpacked' : pl.String, polars expression
            - Polars expression to validate unpacked data.
        - 'downstream_version' : pl.Categorical
            - Version of downstream library used to curate data items.

    result_schema : Literal['coerce', 'relax', 'shrink'], default 'coerce'
        How should dtypes in the output DataFrame be handled?

        - 'coerce' : cast all columns to output schema.
        - 'relax' : keep all columns as-is.
        - 'shrink' : cast columns to smallest possible types.

    Returns
    -------
    pl.DataFrame
        Processed DataFrame with unpacked and decoded data fields, one row per
        dstream buffer

        Output schema:
            - 'dstream_algo' : pl.Categorical
                - Name of downstream curation algorithm used.
                - e.g., 'dstream.steady_algo'
            - 'dstream_data_id' : pl.UInt64
                - Row index identifier for dstream buffer.
            - 'dstream_S' : pl.UInt32
                - Capacity of dstream buffer, in number of data items.
            - 'dstream_T' : pl.UInt64
                - Logical time elapsed (number of elapsed data items in stream).
            - 'dstream_T_dilation' : pl.UInt32
                - Dilation factor applied to T counter; if none, then 1.
            - 'dstream_T_raw' : pl.UInt64
                - Raw packed time counter value, before un-dilation.
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
    logging.info("begin explode_lookup_unpacked")
    logging.info(" - prepping data...")

    _check_df(df)
    if df.lazy().limit(1).collect().is_empty():
        return _make_empty()

    logging.info(" - casting data_hex and dstream_algo...")
    df = df.cast({"data_hex": pl.String, "dstream_algo": pl.Categorical})

    logging.info(" - collecting schema names...")
    schema_names = df.lazy().collect_schema().names()

    if "dstream_T_dilation" in schema_names:
        logging.info(" - found dstream_T_dilation...")
    else:
        logging.info(" - defaulting dstream_T_dilation...")
        df = df.with_columns(dstream_T_dilation=pl.lit(1).cast(pl.UInt32))

    if "downstream_validate_packed" in df:
        logging.info(" - evaluating `downstream_validate_packed` exprs...")
        df = _perform_validations(df, "downstream_validate_packed")

    if "downstream_filter_packed" in df:
        logging.info(" - applying `downstream_filter_packed` exprs...")
        df = _apply_filters(df, "downstream_filter_packed")

    logging.info(" - calculating offsets...")
    df = _calculate_offsets(df)

    if "dstream_data_id" not in df.lazy().collect_schema().names():
        df = df.with_row_index("dstream_data_id")

    logging.info(" - extracting T and storage_hex from data_hex...")
    df = _extract_from_data_hex(df)

    logging.info(" - un-dilating T...")
    df = df.with_columns(
        dstream_T_raw=pl.col("dstream_T"),
    ).with_columns(
        dstream_T=pl.col("dstream_T") // pl.col("dstream_T_dilation"),
    )

    if "downstream_validate_unpacked" in df:
        logging.info(" - evaluating `downstream_validate_unpacked` exprs...")
        df = _perform_validations(df, "downstream_validate_unpacked")

    if "downstream_filter_unpacked" in df:
        logging.info(" - applying `downstream_filter_unpacked` exprs...")
        df = _apply_filters(df, "downstream_filter_unpacked")

    if "downstream_exclude_unpacked" in df:
        logging.info(" - dropping excluded rows...")
        df = _drop_excluded_rows(df)

    logging.info(" - finalizing result schema...")
    df = _finalize_result_schema(df, result_schema)

    logging.info("unpack_data_packed complete")
    return df
