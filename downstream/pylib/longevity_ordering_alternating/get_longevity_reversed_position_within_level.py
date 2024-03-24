from ..longevity_ordering_common import get_longevity_num_positions_at_level


def get_longevity_reversed_position_within_level(
    position_within_level: int,
    longevity_level: int,
) -> int:
    num_positions_within_level = get_longevity_num_positions_at_level(
        longevity_level,
    )
    reversed_position_within_level = (
        num_positions_within_level - 1 - position_within_level
    )
    return reversed_position_within_level
