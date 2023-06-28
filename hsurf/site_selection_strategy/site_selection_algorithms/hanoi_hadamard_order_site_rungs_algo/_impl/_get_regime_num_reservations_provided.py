from deprecated.sphinx import deprecated

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
    thresh = get_regime_reservation_downgrade_rank(
        hanoi_value, surface_size, rank
    )
    before_thresh_num = get_regime_num_reservations_available(
        hanoi_value, surface_size, rank
    )
    if rank >= thresh:
        return before_thresh_num // 2
    else:
        return before_thresh_num
