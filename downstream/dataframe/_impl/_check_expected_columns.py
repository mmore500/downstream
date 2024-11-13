import typing

import polars as pl


def check_expected_columns(
    df: pl.DataFrame,
    expected_columns: typing.Iterable[str],
) -> None:
    missing_columns = set(expected_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Dataframe missing columns: {missing_columns}")
