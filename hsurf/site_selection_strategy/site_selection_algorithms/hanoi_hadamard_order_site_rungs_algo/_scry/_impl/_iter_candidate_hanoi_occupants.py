import typing

from deprecated import deprecated

from ._iter_candidate_reservation_sizes import iter_candidate_reservation_sizes


@deprecated(reason="Uses generator form, needs refactor to functional impl.")
def iter_candidate_hanoi_occupants(
    site: int,
    rank: int,
) -> typing.Iterator[int]:
    # this is going BACK in time
    for candidate_reservation_size in iter_candidate_reservation_sizes(
        site,
        rank,
    ):
        candidate_hanoi_value = site % candidate_reservation_size
        yield candidate_hanoi_value
