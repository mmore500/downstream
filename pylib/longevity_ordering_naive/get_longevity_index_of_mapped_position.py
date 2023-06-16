from ..longevity_ordering_common import (
    get_longevity_level_of_mapped_position,
    get_longevity_num_positions_at_lower_levels,
)
from .get_longevity_position_within_level import (
    get_longevity_position_within_level,
)

def get_longevity_index_of_mapped_position(
    mapped_position: int,
    num_positions: int,
) -> int:
    position_within_level = get_longevity_position_within_level(
        mapped_position,
        num_positions,
    )

    longevity_level = get_longevity_level_of_mapped_position(
        mapped_position,
        num_positions,
    )
    num_positions_at_lower_levels = get_longevity_num_positions_at_lower_levels(
        longevity_level,
    )

    index = position_within_level + num_positions_at_lower_levels
    return index
