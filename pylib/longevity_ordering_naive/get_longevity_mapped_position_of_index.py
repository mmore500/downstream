from ..get_powersof2triangle_val_at_index import (
    get_powersof2triangle_val_at_index,
)
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
    position_within_level = (
        get_powersof2triangle_val_at_index(index - 1) if index else 0
    )

    offset = get_longevity_offset_of_level(longevity_level, num_indices)
    spacing = offset * 2
    position = offset + spacing * position_within_level
    return position
