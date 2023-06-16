from ..longevity_ordering_common import (
    get_longevity_level_of_mapped_position,
    get_longevity_offset_of_level,
)

from .get_longevity_directionality import get_longevity_directionality
from .get_longevity_reversed_position_within_level import (
    get_longevity_reversed_position_within_level,
)


def get_longevity_index_of_mapped_position(
    mapped_position: int,
    num_positions: int,
    polarity: bool,
) -> int:
    longevity_level = get_longevity_level_of_mapped_position(
        mapped_position,
        num_positions,
    )

    offset = get_longevity_offset_of_level(longevity_level, num_positions)
    spacing = offset * 2

    assert spacing == 0 or (mapped_position - offset) % spacing == 0

    directionality = get_longevity_directionality(longevity_level, polarity)
    position_within_level = (mapped_position - offset) // spacing if spacing else 0
    if not directionality:
        position_within_level = get_longevity_reversed_position_within_level(
            position_within_level, longevity_level
        )

    # level -> num_positions_at_lower_levels
    # 0 -> 0
    # 1 -> 1
    # 2 -> 2, etc.
    # 3 -> 4, etc.
    num_positions_at_lower_levels = 2 ** (longevity_level - 1) if longevity_level else 0

    index = position_within_level + num_positions_at_lower_levels
    return index
