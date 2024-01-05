import sys

from deprecated.sphinx import deprecated

from .....pylib import fast_pow2_divide, fast_pow2_mod, hanoi
from ._get_regime_num_reservations_available import (
    get_regime_num_reservations_available,
)
from ._get_safe_downgrade_rank import get_safe_downgrade_rank
from ._get_upcoming_hanoi_invasion_rank import get_upcoming_hanoi_invasion_rank


@deprecated(
    reason="Should rename 'regime' to follow 'term' rung terminology.",
    version="0.0.0",
)
def get_regime_reservation_downgrade_rank(
    hanoi_value: int, surface_size: int, rank: int
) -> int:
    """Implemenentation detail.

    Used in non-fractional reservation incrementing mode (when fractional
    incrementing is not eligible). Sets transition rank where pending
    incidence reservation buffer size count halving occurs.
    """
    cadence = hanoi.get_hanoi_value_index_cadence(hanoi_value)
    offset = hanoi.get_hanoi_value_index_offset(hanoi_value)
    big_tour_size = get_regime_num_reservations_available(
        hanoi_value,
        surface_size,
        rank,
    )
    if big_tour_size == 1:
        return sys.maxsize
    big_tour_time = big_tour_size * cadence
    end_rank = get_upcoming_hanoi_invasion_rank(hanoi_value, rank)
    assert end_rank

    cycle_num_ranks = big_tour_time
    required_cycle_rank_position = fast_pow2_divide(big_tour_time, 2) - cadence
    assert fast_pow2_mod(required_cycle_rank_position, cadence) == 0
    assert required_cycle_rank_position < cycle_num_ranks
    required_lag = fast_pow2_divide(big_tour_time, 2)
    assert fast_pow2_mod(required_lag, cadence) == 0

    downgrade_rank = get_safe_downgrade_rank(
        cycle_num_ranks=cycle_num_ranks,
        required_cycle_rank_position=required_cycle_rank_position,
        required_lag=required_lag,
        end_rank=end_rank,
        hanoi_offset=offset,
        cadence_for_asserts=cadence,
        hanoi_value_for_asserts=hanoi_value,
    )
    assert downgrade_rank <= end_rank
    # note: negative downgrade rank ok...
    # taken to indicate that downgrade should occur immediately (i.e., rank 0)
    return downgrade_rank
