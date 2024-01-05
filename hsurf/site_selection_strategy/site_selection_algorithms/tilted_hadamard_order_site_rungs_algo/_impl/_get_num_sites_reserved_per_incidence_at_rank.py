from ..... import pylib


def get_num_sites_reserved_per_incidence_at_rank(rank: int) -> int:
    """How many surface sites are reserved for per hanoi value incidence, not
    taking into account any gradual dwindling associated with incrementation or
    fractional incrementation?

    Put another way, how far apart are incidence reservation buffer sites
    associated with hanoi value zero?

    Recall that the size of an incidence reservation determines the number of
    distinct hanoi values for which a particular hanoi value incidence will be
    stored.

    Assumes the naive protocol where all incidence reservations are immediately
    halved at the outset of each reservation-size-doubling cycle (i.e., no
    incrementation or fractional incrementation).

    Closely related to `get_num_reservations_provided`.
    """
    return pylib.bit_ceil(
        pylib.hanoi.get_max_hanoi_value_through_index(rank) + 1
    )
