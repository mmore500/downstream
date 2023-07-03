import typing

from deprecated import deprecated

from ......pylib import longevity_ordering_descending as hadamard_order
from ._iter_candidate_reservation_sizes import iter_candidate_reservation_sizes


@deprecated(reason="Uses generator form, needs refactor to functional impl.")
def iter_candidate_reservation_indices(
    site: int,
    surface_size: int,
    rank: int,
) -> typing.Iterator[int]:
    """Yield the possible semantic incidence reservation buffer positions of
    the site `site` under possible candidate reservation sizes from current
    naive size back in time through the minimum, starting reservation size
    (i.e., one site)."""

    # this is going BACK in time
    for candidate_reservation_size in iter_candidate_reservation_sizes(rank):
        candidate_reservation_position = site // candidate_reservation_size
        candidate_reservation_index = (
            hadamard_order.get_longevity_index_of_mapped_position(
                candidate_reservation_position,
                surface_size // candidate_reservation_size,
            )
        )
        yield candidate_reservation_index
