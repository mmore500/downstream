import sys
import typing

from deprecated.sphinx import deprecated

from .....pylib import calc_dyadic_lcm_upper_bound, fast_pow2_mod, hanoi
from ._get_safe_downgrade_rank import get_safe_downgrade_rank


@deprecated(
    reason="Needs rename to follow 'site rung' terminology.",
    version="0.0.0",
)
def get_fractional_downgrade_rank(
    hanoi_value: int,
    surface_size: int,
    rank: int,
    fractional_downgrade_state: typing.Dict,
) -> int:
    """At what rank should reservations provided drop down to the next-lower
    rung (i.e., decrease by one) under the fractional incrementation mode?

    Manages timing to ensure "safe" transitions so that the oldest values are
    contained within dropped incidence reservation buffer positions.
    """
    state = fractional_downgrade_state

    cadence = hanoi.get_hanoi_value_index_cadence(hanoi_value)
    offset = hanoi.get_hanoi_value_index_offset(hanoi_value)
    big_tour_size = calc_dyadic_lcm_upper_bound(
        state["tour size"] - state["current subtrahend"],
        state["tour size"] - state["next subtrahend"],
    )

    if state["tour size"] == 1:
        return sys.maxsize
    big_tour_time = big_tour_size * cadence
    end_rank = state["upcoming invader rank"]
    assert end_rank

    cycle_num_ranks = big_tour_time
    required_cycle_rank_position = 0

    assert fast_pow2_mod(required_cycle_rank_position, cadence) == 0
    assert required_cycle_rank_position < cycle_num_ranks
    required_lag = (state["tour size"] - state["next subtrahend"]) * cadence
    assert fast_pow2_mod(required_lag, cadence) == 0
    res = get_safe_downgrade_rank(
        cycle_num_ranks=cycle_num_ranks,
        required_cycle_rank_position=required_cycle_rank_position,
        required_lag=required_lag,
        end_rank=end_rank,
        hanoi_offset=offset,
        cadence_for_asserts=cadence,
        hanoi_value_for_asserts=hanoi_value,
    )

    assert res > state["upcoming invader rank"] - state["invader cadence"]
    assert res <= state["upcoming invader rank"]
    assert res > 0
    return res
