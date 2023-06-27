from deprecated.sphinx import deprecated

from ._get_num_incidence_reservations_at_rank import (
    get_num_incidence_reservations_at_rank,
)
from ._get_regime_mx import get_regime_mx


@deprecated(
    reason="Should rename 'regime.'",
    version="0.0.0",
)
def get_regime_num_reservations_available(
    hanoi_value: int, surface_size: int, rank: int
) -> int:
    """Implemenentation detail.

    Used in non-fractional reservation incrementing mode (when fractional
    incrementing is not eligible). Controls halving of reservation upon hanoi
    invasion.
    """
    mx = get_regime_mx(hanoi_value, rank)
    return get_num_incidence_reservations_at_rank(rank, surface_size) * mx
