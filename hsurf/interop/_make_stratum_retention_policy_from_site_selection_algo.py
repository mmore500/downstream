import typing

from hstrat.stratum_retention_strategy.stratum_retention_algorithms._detail import (
    PolicyCouplerBase,
    PolicyCouplerFactory,
    PolicySpecBase,
)
import more_itertools as mit


def make_stratum_retention_policy_from_site_selection_algo(
    site_selection_algo: typing.Any,  # TODO type hint module
) -> PolicyCouplerBase:
    """Create object infrastructure for a stratum retention policy equivalent
    to provided surface site selection algorithm."""

    class PolicySpec(PolicySpecBase):
        """Contains all policy parameters, if any."""

        _surface_size: int

        def __init__(
            self: "PolicySpec",
            surface_size: int,
        ):
            """Construct the policy spec.

            Parameters
            ----------
            surface_size : int
                How many sites does surface contain?
            """
            assert surface_size > 1
            self._surface_size = surface_size

        def __eq__(self: "PolicySpec", other: typing.Any) -> bool:
            return isinstance(other, self.__class__) and (
                self._surface_size,
            ) == (other._surface_size,)

        def __repr__(self: "PolicySpec") -> str:
            return f"""{
                self.GetAlgoIdentifier()
            }.{
                PolicySpec.__qualname__
            }(surface_size={
                self._surface_size
            })"""

        def __str__(self: "PolicySpec") -> str:
            return f"""{
                self.GetAlgoTitle()
            } (surface size: {
                self._surface_size
            })"""

        def GetEvalCtor(self: "PolicySpec") -> str:
            return (
                "hsurf.interop.stratum_retention_interop_"
                f"{site_selection_algo.__name__}.{self!r}"
            )

        def GetSurfaceSize(self: "PolicySpec") -> int:
            return self._surface_size

        @staticmethod
        def GetAlgoIdentifier() -> str:
            """Get programatic name for underlying retention algorithm."""
            return site_selection_algo.__name__

        @staticmethod
        def GetAlgoTitle() -> str:
            """Get human-readable name for underlying retention algorithm."""
            return site_selection_algo.__name__.replace("_", " ")

    class CalcNumStrataRetainedExactFtor:
        def __init__(
            self: "CalcNumStrataRetainedExactFtor",
            policy_spec: typing.Optional[PolicySpec],
        ) -> None:
            pass

        def __eq__(
            self: "CalcNumStrataRetainedExactFtor",
            other: typing.Any,
        ) -> bool:
            return isinstance(other, self.__class__)

        def __call__(
            self: "CalcNumStrataRetainedExactFtor",
            policy: PolicyCouplerBase,
            num_strata_deposited: int,
        ) -> int:
            return sum(
                1 for __ in policy.IterRetainedRanks(num_strata_deposited)
            )

    class CalcRankAtColumnIndexFtor:
        def __init__(
            self: "CalcRankAtColumnIndexFtor",
            policy_spec: typing.Optional[PolicySpec],
        ) -> None:
            pass

        def __eq__(
            self: "CalcRankAtColumnIndexFtor",
            other: typing.Any,
        ) -> bool:
            return isinstance(other, self.__class__)

        def __call__(
            self: "CalcRankAtColumnIndexFtor",
            policy: PolicyCouplerBase,
            index: int,
            num_strata_deposited: int,
        ) -> int:
            return mit.nth(
                policy.IterRetainedRanks(num_strata_deposited), index
            )

    class GenDropRanksFtor:
        def __init__(
            self: "GenDropRanksFtor",
            policy_spec: typing.Optional[PolicySpec],
        ) -> None:
            pass

        def __eq__(
            self: "GenDropRanksFtor",
            other: typing.Any,
        ) -> bool:
            return isinstance(other, self.__class__)

        def __call__(
            self: "GenDropRanksFtor",
            policy: PolicyCouplerBase,
            num_stratum_depositions_completed: int,
        ) -> typing.Iterator[int]:
            if num_stratum_depositions_completed == 0:
                return

            algo = site_selection_algo
            surface_size = policy.GetSpec().GetSurfaceSize()

            target_site = algo.pick_deposition_site(
                num_stratum_depositions_completed, surface_size
            )
            target_rank = algo.calc_resident_deposition_rank(
                target_site, surface_size, num_stratum_depositions_completed - 1
            )
            if target_rank != 0:
                yield target_rank
                return

            if num_stratum_depositions_completed + 1 >= surface_size:
                prev_ranks = algo.iter_resident_deposition_ranks(
                    surface_size,
                    num_stratum_depositions_completed - 1,
                )
                next_ranks = algo.iter_resident_deposition_ranks(
                    surface_size,
                    num_stratum_depositions_completed,
                )
                lost_ranks = set(prev_ranks) - set(next_ranks)
                # one deposition is at most one rank lost
                assert len(lost_ranks) <= 1
                yield from lost_ranks

    class IterRetainedRanksFtor:
        def __init__(
            self: "IterRetainedRanksFtor",
            policy_spec: typing.Optional[PolicySpec],
        ) -> None:
            pass

        def __eq__(
            self: "IterRetainedRanksFtor",
            other: typing.Any,
        ) -> bool:
            return isinstance(other, self.__class__)

        def __call__(
            self: "IterRetainedRanksFtor",
            policy: PolicyCouplerBase,
            num_strata_deposited: int,
        ) -> typing.Iterator[int]:
            if num_strata_deposited == 0:
                return
            algo = site_selection_algo
            surface_size = policy.GetSpec().GetSurfaceSize()
            ranks = sorted(
                algo.iter_resident_deposition_ranks(
                    surface_size,
                    num_strata_deposited,
                )
            )
            last_zero = ranks.count(0) - (ranks[0] == 0)
            assert 0 <= last_zero < len(ranks)
            yield from ranks[last_zero:]

    class CalcNumStrataRetainedUpperBoundFtor:
        def __init__(
            self: "CalcNumStrataRetainedUpperBoundFtor",
            policy_spec: typing.Optional[PolicySpec],
        ) -> None:
            pass

        def __eq__(
            self: "CalcNumStrataRetainedUpperBoundFtor",
            other: typing.Any,
        ) -> bool:
            return isinstance(other, self.__class__)

        def __call__(
            self: "CalcNumStrataRetainedUpperBoundFtor",
            policy: PolicyCouplerBase,
            num_strata_deposited: int,
        ) -> typing.Iterator[int]:
            surface_size = policy.GetSpec().GetSurfaceSize()
            return min(
                num_strata_deposited,
                surface_size,
            )

    return PolicyCouplerFactory(
        policy_spec_t=PolicySpec,
        gen_drop_ranks_ftor_t=GenDropRanksFtor,
        calc_num_strata_retained_exact_ftor_t=CalcNumStrataRetainedExactFtor,
        calc_rank_at_column_index_ftor_t=CalcRankAtColumnIndexFtor,
        iter_retained_ranks_ftor_t=IterRetainedRanksFtor,
        calc_num_strata_retained_upper_bound_ftor_t=CalcNumStrataRetainedUpperBoundFtor,
    )
