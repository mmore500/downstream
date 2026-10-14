import os
import typing


def choose_pl_engine(
    *,
    prefer: typing.Literal["in-memory", "streaming"],
) -> str:
    """Choose Polars engine, using `prefer` unless overridden by the
    `POLARS_ENGINE_AFFINITY` environment variable."""
    if os.environ.get("POLARS_ENGINE_AFFINITY"):
        return "auto"  # polars resolves "auto" using POLARS_ENGINE_AFFINITY
    return prefer
