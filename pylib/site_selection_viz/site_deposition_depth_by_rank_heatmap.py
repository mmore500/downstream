import typing

from matplotlib import axes as mpl_axes
from matplotlib import colors as mpl_colors
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

from ..Literal import Literal
from ._apply_pseudo_linear_yticks import apply_pseudo_linear_yticks
from ._apply_pseudo_log_yticks import apply_pseudo_log_yticks
from ._geomspace_filter_surface_history_df import (
    geomspace_filter_surface_history_df,
)
from ._linspace_filter_surface_history_df import (
    linspace_filter_surface_history_df,
)


def site_deposition_depth_by_rank_heatmap(
    surface_history_df: pd.DataFrame,
    cnorm: typing.Optional[Literal["log"]] = "log",
    ynorm: typing.Optional[Literal["log", "linear"]] = "log",
    rank_sample_size: int = 256,
    figsize: typing.Tuple[int, int] = (12, 7),
) -> mpl_axes.Axes:
    # Reshape DataFrame
    if ynorm == "log":
        filtered_df = geomspace_filter_surface_history_df(
            surface_history_df,
            rank_sample_size,
        )
    else:
        assert ynorm in ("linear", None)
        filtered_df = linspace_filter_surface_history_df(
            surface_history_df,
            rank_sample_size,
        )

    reshaped_df = filtered_df.pivot_table(
        index="rank",
        columns="site",
        values="deposition depth",
    )

    # Create heatmap
    plt.figure(figsize=(12, 7))
    if cnorm == "log":
        cnorm = mpl_colors.SymLogNorm(linthresh=1.0)
    else:
        assert cnorm is None
    ax = sns.heatmap(
        reshaped_df,
        annot=False,
        cmap="viridis",
        norm=cnorm,
    )

    if ynorm == "log":
        ax = apply_pseudo_log_yticks(ax)
    elif ynorm == "linear":
        ax = apply_pseudo_linear_yticks(ax)
    else:
        assert ynorm is None

    return ax
