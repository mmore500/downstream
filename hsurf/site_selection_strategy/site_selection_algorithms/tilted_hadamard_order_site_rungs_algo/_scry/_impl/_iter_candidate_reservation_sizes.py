import typing

from deprecated import deprecated

from ..._impl._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)


@deprecated(reason="Uses generator form, needs refactor to functional impl.")
def iter_candidate_reservation_sizes(rank: int) -> typing.Iterator[int]:
    """Yield the incidence reservation sizes from current naive size back in
    time through the minimum, starting reservation size (i.e., one site).

    Reservation size refers to the number of sites reserved per hanoi incidence,
    from the point of view of a particular hanoi value. More precisely, the
    surface size divided by the bit ceiling of the incidence buffer size for a
    hanoi value.
    """

    # this is the maximum (current) reservation size, a perfect power of 2
    naive_reservation_size = get_num_sites_reserved_per_incidence_at_rank(rank)

    reservation_size = naive_reservation_size
    # this is going BACK in time, with reservation size halving repeatedly
    while reservation_size:
        yield reservation_size
        reservation_size >>= 1  # equiv //= 2
