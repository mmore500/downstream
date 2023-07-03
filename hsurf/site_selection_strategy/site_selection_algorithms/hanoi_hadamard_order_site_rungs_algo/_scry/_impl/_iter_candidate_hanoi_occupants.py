import typing

from deprecated import deprecated

from ._iter_candidate_reservation_sizes import iter_candidate_reservation_sizes


@deprecated(reason="Uses generator form, needs refactor to functional impl.")
def iter_candidate_hanoi_occupants(
    site: int,
    rank: int,
) -> typing.Iterator[int]:
    """Yield the possible hanoi values that would be associated with the site
    `site` under possible candidate reservation sizes from current
    naive size back in time through the minimum, starting reservation size
    (i.e., one site).

    Note that yielded candidate hanoi values may not have yet been deposited
    at the site (or ever be deposited at the site) due to insufficient
    depositoins of that hanoi value to actually reach the candidate semantic
    incidence reservation ring buffer position that would be associated with
    `site` at `rank` given the candidate reservation size. (See
    `iter_candidate_reservation_indices`.)
    """

    # this is going BACK in time
    for candidate_reservation_size in iter_candidate_reservation_sizes(rank):
        candidate_hanoi_value = site % candidate_reservation_size
        yield candidate_hanoi_value
