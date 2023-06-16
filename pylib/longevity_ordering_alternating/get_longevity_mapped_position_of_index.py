from ..longevity_ordering_common import (
    get_longevity_level_of_index,
    get_longevity_offset_of_level,
)
from ..get_powersof2triangle_val_at_index import get_powersof2triangle_val_at_index

from .get_longevity_directionality import get_longevity_directionality
from .get_longevity_reversed_position_within_level import (
    get_longevity_reversed_position_within_level,
)


def get_longevity_mapped_position_of_index(
    index: int,
    num_indices: int,
    polarity: bool,
) -> int:
    longevity_level = get_longevity_level_of_index(index)
    position_within_level = (
        get_powersof2triangle_val_at_index(index - 1) if index else 0
    )

    directionality = get_longevity_directionality(longevity_level, polarity)
    offset = get_longevity_offset_of_level(longevity_level, num_indices)
    spacing = offset * 2
    if not directionality:
        position_within_level = (
            get_longevity_reversed_position_within_level(
                position_within_level,
                longevity_level,
            )
        )
    position = offset + spacing * position_within_level
    return position
