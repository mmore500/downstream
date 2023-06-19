import numpy as np
import pandas as pd


def linspace_filter_surface_history_df(
    surface_history_df: pd.DataFrame,
    rank_sample_size: int,
) -> pd.DataFrame:

    filtered_df = surface_history_df[
        surface_history_df["rank"].isin(
            {
                *np.linspace(
                    1,
                    surface_history_df["rank"].max(),
                    num=rank_sample_size,
                    dtype=int,
                )
            },
        )
    ]
    return filtered_df
