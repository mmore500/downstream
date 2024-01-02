import functools

from deprecated.sphinx import deprecated

from ._get_fractional_downgrade_num_reservations_provided import (
    get_fractional_downgrade_num_reservations_provided,
)
from ._get_fractional_downgrade_state import get_fractional_downgrade_state
from ._get_regime_num_reservations_provided import (
    get_regime_num_reservations_provided,
)


@deprecated(
    reason="Needs rename to follow 'site rung' terminology.",
    version="0.0.0",
)
@functools.lru_cache(maxsize=8192)  # optimization, not functionally necessary
def get_num_reservations_provided(
    hanoi_value: int, surface_size: int, rank: int
) -> int:
    """Determine incidence reservation buffer positions provided for
    depositions associated with `hanoi_value` at rank `rank`, under fractional
    incrementaiton if eligible and otherwise falling back to coarser non-
    fractional incrementation."""
    fractional_downgrade_state = get_fractional_downgrade_state(
        hanoi_value, surface_size, rank
    )
    if fractional_downgrade_state is not None:
        return get_fractional_downgrade_num_reservations_provided(
            hanoi_value,
            surface_size,
            rank,
            fractional_downgrade_state,
        )
    else:
        return get_regime_num_reservations_provided(
            hanoi_value, surface_size, rank
        )
