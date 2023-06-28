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
