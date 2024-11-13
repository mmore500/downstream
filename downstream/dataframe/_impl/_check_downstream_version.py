import warnings

import polars as pl

from ..._version import __version__ as downstream_version


def check_downstream_version(df: pl.DataFrame) -> None:
    """Check the 'downstream_version' column in the DataFrame for consistency
    with the library major version.

    This function performs several checks on the 'downstream_version' column of the provided DataFrame:
    - Issues a warning if the 'downstream_version' column is not provided.
    - Issues a warning if multiple 'downstream_version' values are detected.
    - Compares the major version of the DataFrame's 'downstream_version' with the expected downstream major version and issues a warning if they do not match.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to be checked, expected to contain a 'downstream_version' column.

    Raises
    ------
    UserWarning
        If the 'downstream_version' column is missing, contains multiple values, or its major version does not match the expected version.
    """
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
