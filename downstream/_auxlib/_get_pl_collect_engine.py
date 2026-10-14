import os


def get_pl_collect_engine() -> str:
    """Choose Polars engine for collecting LazyFrames.

    Polars 2.x defaults lazy queries to the streaming engine, which can be
    dramatically slower for the repeated collects performed on wide
    concatenated scans (e.g., many input files via CLI). Default to the
    in-memory engine, but defer to the user's `POLARS_ENGINE_AFFINITY`
    environment variable if set.

    Returns
    -------
    str
        Value for the `engine` kwarg of `LazyFrame.collect` and
        `pl.collect_all`.
    """
    if os.environ.get("POLARS_ENGINE_AFFINITY"):
        return "auto"  # polars resolves "auto" using POLARS_ENGINE_AFFINITY
    return "in-memory"
