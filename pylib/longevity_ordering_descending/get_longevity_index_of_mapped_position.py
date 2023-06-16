from .. import longevity_ordering_naive as lon
from ..oeis import get_a341916_value_at_index


def get_longevity_index_of_mapped_position(
    mapped_position: int,
    num_positions: int,
) -> int:

    naive_index = lon.get_longevity_index_of_mapped_position(
        mapped_position,
        num_positions,
    )
    return get_a341916_value_at_index(naive_index)
