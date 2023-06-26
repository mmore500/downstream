from ..bit_floor import bit_floor
from ..longevity_ordering_common import (
    get_longevity_level_of_index,
    get_longevity_offset_of_level,
)


# related to https://oeis.org/A181733
# see also https://oeis.org/A139709 and https://oeis.org/A092323
def get_longevity_mapped_position_of_index(
    index: int, num_indices: int
) -> int:
    longevity_level = get_longevity_level_of_index(index)

    # see get_powersof2triangle_val_at_index
    position_within_level = index - bit_floor(index)

    offset = get_longevity_offset_of_level(longevity_level, num_indices)
    spacing = offset << 1
    return offset + spacing * position_within_level
