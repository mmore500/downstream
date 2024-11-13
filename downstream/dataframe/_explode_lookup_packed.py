import typing

import polars as pl

from ._explode_lookup_unpacked import explode_lookup_unpacked
from ._unpack_data_packed import unpack_data_packed


def explode_lookup_packed(
    df: pl.DataFrame,
    *,
    value_type: typing.Literal["hex", "uint64", "uint32", "uint16", "uint8"],
) -> pl.DataFrame:
    """Explode downstream-curated data from hexidecimal serialization of
    downstream buffers and counters to one-data-item-per-row, applying
    downstream lookup to identify origin time `Tbar` of each item."""
    df = unpack_data_packed(df)
    return explode_lookup_unpacked(df, value_type=value_type)
