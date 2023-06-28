from deprecated import deprecated

from ......pylib import hanoi
from ._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)


# is this redundant with get_regime_mx?
@deprecated(
    reason="Redundant to other implementation logic; should consolidate."
)
def is_2x_reservation_eligible(
    hanoi_value: int, surface_size: int, rank: int
) -> bool:
    """Controls degradation of reservation space available after hanoi
    invasion.

    Relic from original reservation-runged approach.
    """
    reservation_width = get_num_sites_reserved_per_incidence_at_rank(rank)
    lb_inclusive = (
        hanoi.get_max_hanoi_value_through_index(rank)
        - reservation_width // 2
        + 1
    )
    ub_exclusive = reservation_width // 2
    return lb_inclusive <= hanoi_value < ub_exclusive
