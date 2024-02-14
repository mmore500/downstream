from ..longevity_ordering_common import (
    get_longevity_level_of_index,
    get_longevity_offset_of_level,
)
from ..oeis import get_a030109_value_at_index


def get_longevity_mapped_position_of_index(
    index: int,
    num_indices: int,
) -> int:
    """Which physical site in the sequence does the `index`th logical entry map
    to?"""
    longevity_level = get_longevity_level_of_index(index)
    position_within_level = (
        get_a030109_value_at_index(index - 1) if index else 0
    )

    offset = get_longevity_offset_of_level(longevity_level, num_indices)
    spacing = offset * 2
    position = offset + spacing * position_within_level
    return position
