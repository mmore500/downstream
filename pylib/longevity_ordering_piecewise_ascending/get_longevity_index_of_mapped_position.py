from .. import longevity_ordering_naive as lon
from ..longevity_ordering_common import (
    get_longevity_level_of_mapped_position,
    get_longevity_num_positions_at_level,
    get_longevity_num_positions_at_lower_levels,
    get_longevity_offset_of_level,
)
from ..oeis import get_a030109_index_of_value


def get_longevity_index_of_mapped_position(
    mapped_position: int,
    num_positions: int,
) -> int:
    longevity_level = get_longevity_level_of_mapped_position(
        mapped_position,
        num_positions,
    )
    naive_position_within_level = lon.get_longevity_position_within_level(
        mapped_position,
        num_positions,
    )
    index = (
        get_a030109_index_of_value(
            naive_position_within_level,
            longevity_level,
        )
        + 1
        if mapped_position
        else 0
    )
    return index
