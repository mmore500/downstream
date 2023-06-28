import typing

from deprecated import deprecated

from ..._impl._get_num_sites_reserved_per_incidence_at_rank import (
    get_num_sites_reserved_per_incidence_at_rank,
)


@deprecated(reason="Uses generator form, needs refactor to functional impl.")
def iter_candidate_reservation_sizes(
    site: int,
    rank: int,
) -> typing.Iterator[int]:
    # this is going BACK in time
    naive_reservation_size = get_num_sites_reserved_per_incidence_at_rank(rank)

    reservation_size = naive_reservation_size
    while reservation_size:
        yield reservation_size
        reservation_size //= 2
