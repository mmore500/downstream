import warnings

import polars as pl

from ..._version import __version__ as downstream_version


def check_downstream_version(df: pl.DataFrame) -> None:
    if "downstream_version" not in df.columns:
        warnings.warn(
            "Dataframe downstream_version column not provided",
        )
    elif df["downstream_version"].unique().len() > 1:
        warnings.warn(
            "Multiple downstream_version values detected",
        )
    elif df["downstream_version"].unique().len() == 0:
        pass
    elif next(iter(df["downstream_version"].item(0).split(".")), None) != next(
        iter(downstream_version.split(".")), None
    ):
        warnings.warn(
            f"Dataframe downstream_version {df['downstream_version'].item(0)} "
            f"does not match downstream major version {downstream_version}",
        )
