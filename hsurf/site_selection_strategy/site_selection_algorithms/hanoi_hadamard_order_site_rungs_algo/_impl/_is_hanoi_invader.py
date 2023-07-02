from ._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)


def is_hanoi_invader(hanoi_value: int, rank: int) -> bool:
    """Is `hanoi_value` currently depositing over sites previously reserved for
    another hanoi value?

    Put another way, is `hanoi_value` currently in the process of depositing
    into sites for the first time to fill its initially-allocated reservation?
    Note that hanoi values are considered invaders even if they will not invade
    during the current reservation-size-doubling cycle.
    """
    reservation_width = get_num_sites_reserved_per_incidence_at_rank(rank)
    return hanoi_value >= reservation_width // 2
