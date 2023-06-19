import typing

import pandas as pd


class SurfaceHistoryToStratumRetentionPolicyShim:

    _surface_history_df: pd.DataFrame

    def __init__(
        self: "SurfaceHistoryToStratumRetentionPolicyShim",
        surface_history_df: pd.DataFrame,
    ) -> None:
        self._surface_history_df = surface_history_df.copy()

    CalcRankAtColumnIndex = None

    def GenDropRanks(
        self: "SurfaceHistoryToStratumRetentionPolicyShim",
        num_stratum_depositions_completed: int,
        retained_ranks: typing.Optional[typing.Iterable[int]],
    ) -> typing.Iterator[int]:
        return iter(
            {*self.IterRetainedRanks(num_stratum_depositions_completed)}
            - {*self.IterRetainedRanks(num_stratum_depositions_completed + 1)}
        )

    def IterRetainedRanks(
        self: "SurfaceHistoryToStratumRetentionPolicyShim",
        num_strata_deposited: int,
    ) -> typing.Iterator[int]:
        at_rank_df = self._surface_history_df[
            self._surface_history_df["rank"] == num_strata_deposited
        ]
        return (
            rank
            for rank in at_rank_df["deposition rank"].unique()
            if rank != -1
        )
