from deprecated.sphinx import deprecated

from .....pylib import fast_pow2_divide, hanoi
from ._get_regime_num_reservations_available import (
    get_regime_num_reservations_available,
)
from ._get_regime_reservation_downgrade_rank import (
    get_regime_reservation_downgrade_rank,
)


@deprecated(
    reason="Should rename 'regime' to follow 'term' rung terminology.",
    version="0.0.0",
)
def get_regime_num_reservations_provided(
    hanoi_value: int, surface_size: int, rank: int
) -> int:
    """How many incidence reservation buffer positions are provided for
    depositions associated with `hanoi_value` at rank `rank` under non-
    fractional reservation incrementing mode (i.e., when fractional
    incrementing is not eligible)?

    Extends `get_regime_num_reservations_available` to time downgrading (i.e.,
    halving the incidence reservation buffer size) so that it occurs "safely"
    when athe most recent deposition is at the last site that will be retained
    after degradation (so the next deposition will be at semantic incidence
    reseration buffer position zero).
    """
    thresh = get_regime_reservation_downgrade_rank(
        hanoi_value, surface_size, rank
    )
    before_thresh_num = get_regime_num_reservations_available(
        hanoi_value, surface_size, rank
    )
    if rank >= thresh:
        return fast_pow2_divide(before_thresh_num, 2)
    else:
        return before_thresh_num
