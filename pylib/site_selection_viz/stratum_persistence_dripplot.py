import typing

from hstrat import hstrat
from matplotlib import axes as mpl_axes
import pandas as pd

from ._SurfaceHistoryToStratumRetentionPolicyShim import (
    SurfaceHistoryToStratumRetentionPolicyShim,
)


def stratum_persistence_dripplot(
    surface_history_df: pd.DataFrame,
    progress_wrap: typing.Callable = lambda x: x,
) -> mpl_axes.Axes:
    policy_shim = SurfaceHistoryToStratumRetentionPolicyShim(
        surface_history_df
    )
    return hstrat.stratum_retention_dripplot(
        policy_shim,
        surface_history_df["rank"].max(),
        progress_wrap=progress_wrap,
    )
