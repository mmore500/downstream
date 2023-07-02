import typing

from deprecated.sphinx import deprecated

from ._get_fractional_downgrade_rank import get_fractional_downgrade_rank


@deprecated(
    reason="Needs rename to follow 'site rung' terminology.",
    version="0.0.0",
)
def get_fractional_downgrade_num_reservations_provided(
    hanoi_value: int,
    surface_size: int,
    rank: int,
    fractional_downgrade_state: typing.Dict,
) -> int:
    """How many incidence reservation buffer positions are provided for
    depositions associated with `hanoi_value` at rank `rank` under fractional
    reservation incrementing mode (i.e., a hanoi value's reservations aren't
    simply halved all at once upon invasion)?

    Compares `rank` to result from `get_fractional_downgrade_rank` to apply
    fine timing to current fractional reservation incrementation state."""
    thresh = get_fractional_downgrade_rank(
        hanoi_value,
        surface_size,
        rank,
        fractional_downgrade_state,
    )

    state = fractional_downgrade_state
    if rank >= thresh:
        return state["tour size"] - state["next subtrahend"]
    else:
        return state["tour size"] - state["current subtrahend"]
