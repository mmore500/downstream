from ..longevity_ordering_common import (
    get_longevity_level_of_mapped_position,
    get_longevity_offset_of_level,
)


def get_longevity_position_within_level(
    mapped_position: int,
    num_positions: int,
) -> int:
    longevity_level = get_longevity_level_of_mapped_position(
        mapped_position,
        num_positions,
    )

    offset = get_longevity_offset_of_level(longevity_level, num_positions)
    spacing = offset * 2

    assert spacing == 0 or (mapped_position - offset) % spacing == 0
    position_within_level = (
        (mapped_position - offset) // spacing if spacing else 0
    )
    return position_within_level
