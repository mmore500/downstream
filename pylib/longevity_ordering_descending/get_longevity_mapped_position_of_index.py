from ..oeis import get_a341916_index_of_value

from ..longevity_ordering_common import (
    get_longevity_level_of_index,
    get_longevity_offset_of_level,
)

def get_longevity_mapped_position_of_index(
    index: int,
    num_indices: int,
) -> int:
    longevity_level = get_longevity_level_of_index(index)

    subtrahend = 2 ** longevity_level // 2
    position_within_level = (
        get_a341916_index_of_value(index)
        - subtrahend
    )
    offset = get_longevity_offset_of_level(longevity_level, num_indices)
    spacing = offset * 2
    position = offset + spacing * position_within_level
    return position
